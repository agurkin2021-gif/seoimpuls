/* Playwright acceptance test: English SEO service selector page, mobile + desktop. */
const fs=require("node:fs"),path=require("node:path");
const {chromium}=require("playwright");
const ORIGIN="http://127.0.0.1:8765", PAGE_URL=ORIGIN+"/seo-services/";
const OUT="audit-artifacts/en-services";
fs.mkdirSync(OUT,{recursive:true});
let browser;
(async()=>{
 browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
 const report={url:PAGE_URL,viewports:[]};
 for(const width of [390,1280]){
  const ctx=await browser.newContext({viewport:{width,height:width===390?844:800},deviceScaleFactor:1,isMobile:width===390,hasTouch:width===390});
  const page=await ctx.newPage(),errors=[],networkFailures=[];
  page.on("pageerror",e=>errors.push(e.message));
  page.on("requestfailed",r=>networkFailures.push({url:r.url(),error:r.failure()?.errorText}));
  console.log("SERVICES_STAGE "+width+" opening page");
  const res=await page.goto(PAGE_URL,{waitUntil:"domcontentloaded",timeout:30000});
  await page.waitForTimeout(550);
  console.log("SERVICES_STAGE "+width+" DOM ready");
  try{await page.screenshot({path:path.join(OUT,width+"-first.png"),timeout:12000,animations:"disabled"});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message.slice(0,120));}
  const reject=page.getByRole("button",{name:/Reject Non-Essential/i});
  if(await reject.count())await reject.first().click({timeout:6000});
  await page.evaluate(()=>document.querySelectorAll("img[loading=lazy]").forEach(x=>x.loading="eager"));
  await page.waitForTimeout(500);
  console.log("SERVICES_STAGE "+width+" cookies handled");
  const data=await page.evaluate(()=>{
   const grid=document.querySelector(".services-hub");
   const images=Array.from(document.images).map(x=>({src:x.currentSrc,ok:x.complete&&x.naturalWidth>0}));
   const links=Array.from(document.querySelectorAll("a[href]")).map(x=>x.href);
   const jsonld=Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(x=>{try{return {valid:true,type:JSON.parse(x.textContent)["@type"]||"graph"};}catch(e){return {valid:false,error:String(e)}}});
   return {
    title:document.title,h1:Array.from(document.querySelectorAll("h1")).map(x=>x.textContent.trim()),
    canonical:document.querySelector('link[rel="canonical"]')?.href||"",
    gridColumns:grid?getComputedStyle(grid).gridTemplateColumns.split(" ").filter(Boolean).length:0,
    cards:Array.from(document.querySelectorAll(".services-hub-card")).map(x=>({label:x.textContent.trim(),href:x.href})),
    intro:document.querySelector(".services-hub__intro")?.textContent.trim()||"",
    footerClass:document.querySelector(".custom-footer")?.className||"",
    socialCount:document.querySelectorAll(".footer-social-icons a").length,
    mapCount:document.querySelectorAll(".footer-map").length,
    contacts:{whatsapp:!!document.querySelector(".footer-shortcut--whatsapp"),telegram:!!document.querySelector(".footer-shortcut--telegram"),email:!!document.querySelector(".js-footer-mail")},
    menu:Array.from(document.querySelectorAll("nav a")).find(x=>x.textContent.trim()==="Services")?.href||"",
    innerWidth,scrollWidth:document.documentElement.scrollWidth,
    images,links,jsonld
   };
  });
  try{await page.screenshot({path:path.join(OUT,width+"-full.png"),fullPage:true,timeout:14000,animations:"disabled"});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message.slice(0,120));}
  // Link QA is deterministic against the Hugo output; do not stall on request loops.
  console.log("SERVICES_STAGE "+width+" DOM diagnostics collected");
  const brokenLinks=[];
  const paths=Array.from(new Set(data.links.filter(u=>u.startsWith(ORIGIN)||u.startsWith("https://seoimpuls.com/")).map(u=>new URL(u).pathname)));
  for(const p of paths){
    const decoded=decodeURIComponent(p);
    const relative=decoded.replace(/^\/+/, "");
    const local=path.join("public",relative,decoded.endsWith("/")?"index.html":"");
    if(!fs.existsSync(local))brokenLinks.push({url:p,file:local});
  }
  console.log("SERVICES_STAGE "+width+" checked "+paths.length+" local routes");
  const fail=[];
  if(res.status()!==200)fail.push("HTTP");
  if(data.h1.length!==1||data.h1[0]!=="SEO Services & Practical Deliverables")fail.push("H1");
  if(!data.title.startsWith("SEO Services & Practical Deliverables | SeoImpuls"))fail.push("Title");
  if(data.canonical!=="https://seoimpuls.com/seo-services/")fail.push("Canonical");
  if(data.cards.length!==3)fail.push("Cards");
  if(data.gridColumns!==(width===390?1:3))fail.push("Grid columns="+data.gridColumns);
  if(!data.intro.startsWith("Compare the three SEO services we offer"))fail.push("Direct answer");
  for(const u of ["/seo/","/services/keyword-research/","/services/seo-consultation/"]){
    if(!data.cards.some(x=>new URL(x.href).pathname===u))fail.push("Missing card "+u);
  }
  if(!data.footerClass.includes("custom-footer--en-services")||data.socialCount||data.mapCount)fail.push("Footer unverifiable links");
  if(!data.contacts.whatsapp||!data.contacts.telegram||!data.contacts.email)fail.push("Contact links");
  if(!data.menu.endsWith("/seo-services/"))fail.push("Nav");
  if(data.scrollWidth>width+2)fail.push("Overflow");
  if(data.images.some(x=>!x.ok))fail.push("Images");
  if(data.jsonld.some(x=>!x.valid))fail.push("JSON-LD");
  if(errors.length||networkFailures.length)fail.push("JavaScript/network");
  if(brokenLinks.length)fail.push("Internal links");
  report.viewports.push({width,status:res.status(),...data,brokenLinks,errors,networkFailures,fail});
  console.log("SERVICES_BROWSER_SUMMARY "+JSON.stringify({width,status:res.status(),h1:data.h1,gridColumns:data.gridColumns,cards:data.cards.length,overflow:data.scrollWidth>width,brokenLinks,errors,networkFailures,fail}));
  await ctx.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(OUT,"audit.json"),JSON.stringify(report,null,2));
 if(report.viewports.some(x=>x.fail.length))throw Error("EN services QA failed");
 console.log("SERVICES_BROWSER_PASS two viewports, no broken links, no fake footer");
})().catch(async e=>{
 console.error("SERVICES_BROWSER_FATAL "+(e.stack||e));
 try{if(browser)await browser.close();}catch(closeError){console.error("SERVICES_BROWSER_CLOSE_WARNING "+closeError.message);}
 process.exitCode=1;
});
