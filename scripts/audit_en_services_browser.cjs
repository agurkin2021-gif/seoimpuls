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
 for(const width of [390,768,1280]){
  const ctx=await browser.newContext({viewport:{width,height:width===390?844:800},deviceScaleFactor:1,isMobile:width===390,hasTouch:width===390});
  const page=await ctx.newPage(),errors=[],networkFailures=[];
  page.on("pageerror",e=>errors.push(e.message));
  page.on("requestfailed",r=>networkFailures.push({url:r.url(),error:r.failure()?.errorText}));
  console.log("SERVICES_STAGE "+width+" opening page");
  const res=await page.goto(PAGE_URL,{waitUntil:"domcontentloaded",timeout:30000});
  await page.waitForTimeout(550);
  console.log("SERVICES_STAGE "+width+" DOM ready");
  try{await page.screenshot({path:path.join(OUT,width+"-first.png"),timeout:12000,animations:"disabled"});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message.slice(0,120));}

  const initialConsent=await page.evaluate(()=>{
    const banner=document.querySelector(".gdpr-consent-banner");
    const actions=banner?.querySelector(".gdpr-consent-actions");
    const style=actions?getComputedStyle(actions):null;
    return {shown:!!banner&&!banner.hidden,layout:style?.display||"",columns:style?.gridTemplateColumns.split(" ").filter(Boolean).length||0,
      buttons:actions?.querySelectorAll("button").length||0,accept:!!actions?.querySelector("#gdprAcceptAll"),reject:!!actions?.querySelector("#gdprReject")};
  });
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
    workstreamCount:document.querySelectorAll(".seo-catalog__workstream").length,
    scopeStatusCounts:Object.fromEntries(["published","component","conditional"].map(k=>[k,document.querySelectorAll('.seo-catalog__workstream [data-scope-status="'+k+'"]').length])),
    scopeLegendPresent:(document.querySelector("#seo-catalog-title + .seo-catalog__lede")?.textContent||"").includes("Six specialized areas require an explicit capability"),
    groupCount:document.querySelectorAll(".seo-catalog__group").length,
    choiceCount:document.querySelectorAll(".seo-catalog__choice").length,
    selectorBeforeCatalogue:(()=>{
      const selector=document.querySelector(".seo-catalog__matching");
      const heading=document.getElementById("seo-catalog-title");
      return !!selector&&!!heading&&!!(selector.compareDocumentPosition(heading)&Node.DOCUMENT_POSITION_FOLLOWING);
    })(),
    jumpLinks:Array.from(document.querySelectorAll(".seo-catalog__toc a[href^='#']")).map(a=>({target:a.getAttribute("href").slice(1),label:a.textContent.trim(),targetExists:!!document.getElementById(a.getAttribute("href").slice(1))})),
    returnLinks:document.querySelectorAll(".seo-catalog__back[href='#seo-catalog-title']").length,
    catalogueScrollMargin:parseFloat(getComputedStyle(document.querySelector("#seo-catalog-title")).scrollMarginTop)||0,
    consultationGraphicCount:document.querySelectorAll(".services-hub-card__consult-visual").length,
    consultMediaImageCount:document.querySelectorAll('.services-hub-card[href$="/services/seo-consultation/"] img').length,
    reportExampleCount:document.querySelectorAll(".seo-catalog__evidence-item").length,
    faqQuestionCount:document.querySelectorAll(".seo-catalog__faq details").length,
    detailLinks:Array.from(document.querySelectorAll(".seo-catalog__detail-link")).map(a=>({text:a.textContent.trim(),href:a.href})),
    categoryScrollMargin:parseFloat(getComputedStyle(document.querySelector("#seo-work-technical")).scrollMarginTop)||0,
    cards:Array.from(document.querySelectorAll(".services-hub-card")).map(x=>({label:x.textContent.trim(),href:x.href})),
    intro:document.querySelector(".services-hub__intro")?.textContent.trim()||"",
    footerClass:document.querySelector(".custom-footer")?.className||"",
    footerGeometry:(()=>{
      const footer=document.querySelector(".custom-footer");
      const header=document.querySelector(".custom-header");
      const f=footer?.getBoundingClientRect(),h=header?.getBoundingClientRect();
      return {position:footer?getComputedStyle(footer).position:"",top:Math.round(f?.top??0),bottom:Math.round(f?.bottom??0),headerBottom:Math.round(h?.bottom??0)};
    })(),
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
  if(data.h1.length!==1||data.h1[0]!=="Choose the Right SEO Work for Your Website")fail.push("H1");
  if(data.title!=="SEO Audits, Keyword Research & Consulting | SeoImpuls")fail.push("Title");
  if(data.canonical!=="https://seoimpuls.com/seo-services/")fail.push("Canonical");
  if(data.cards.length!==3)fail.push("Cards");
  if(data.workstreamCount!==23||data.groupCount!==4||data.choiceCount!==3)fail.push("Workstream scope");
  if(data.scopeStatusCounts.published!==3||data.scopeStatusCounts.component!==14||data.scopeStatusCounts.conditional!==6||!data.scopeLegendPresent)fail.push("Commercial truth and capability labels");
  if(!data.selectorBeforeCatalogue)fail.push("Buyer choice must precede workstream directory");
  if(data.jumpLinks.length!==5||data.jumpLinks.some(x=>!x.targetExists))fail.push("Category navigation");
  if(data.returnLinks!==4||data.catalogueScrollMargin<100)fail.push("Return navigation");
  if(width===390 && initialConsent.shown && (initialConsent.layout!=="grid"||initialConsent.columns!==2||initialConsent.buttons!==3||!initialConsent.accept||!initialConsent.reject))fail.push("Mobile consent action layout");
  if(data.consultationGraphicCount!==1||data.consultMediaImageCount!==0)fail.push("Repeated consultation image");
  if(data.reportExampleCount!==4)fail.push("Evidence example");
  if(data.faqQuestionCount!==5)fail.push("Buyer FAQ coverage");
  if(data.detailLinks.length!==3||data.detailLinks.some(x=>!x.text.startsWith("Review ")))fail.push("Descriptive workstream links");
  if(data.categoryScrollMargin<100)fail.push("Section scroll margin");
  if(data.gridColumns!==(width===390?1:width===768?2:3))fail.push("Grid columns="+data.gridColumns);
  if(!data.intro.startsWith("Choose the right starting point"))fail.push("Direct answer");
  for(const u of ["/seo/","/services/keyword-research/","/services/seo-consultation/"]){
    if(!data.cards.some(x=>new URL(x.href).pathname===u))fail.push("Missing card "+u);
  }
  if(!data.footerClass.includes("custom-footer--en-services")||data.socialCount||data.mapCount)fail.push("Footer unverifiable links");
  if(width===768&&(data.footerGeometry.position!=="fixed"||data.footerGeometry.top<data.footerGeometry.headerBottom))fail.push("768px footer overlaps header and logo");
  if(!data.contacts.whatsapp||!data.contacts.telegram||!data.contacts.email)fail.push("Contact links");
  if(!data.menu.endsWith("/seo-services/"))fail.push("Nav");
  if(data.scrollWidth>width+2)fail.push("Overflow");
  if(data.images.some(x=>!x.ok))fail.push("Images");
  if(data.jsonld.some(x=>!x.valid)||!data.jsonld.some(x=>x.type==="BreadcrumbList")||data.jsonld.some(x=>x.type==="BlogPosting"))fail.push("JSON-LD");
  if(errors.length||networkFailures.length)fail.push("JavaScript/network");
  if(brokenLinks.length)fail.push("Internal links");

  // A real hash jump must not place its section heading underneath the fixed header.
  await page.evaluate(()=>document.getElementById("seo-work-technical").scrollIntoView({block:"start",behavior:"instant"}));
  await page.waitForTimeout(200);
  const scrollCheck=await page.evaluate(()=>({
    sectionTop:Math.round(document.getElementById("seo-work-technical").getBoundingClientRect().top),
    headerBottom:Math.round(document.querySelector(".custom-header")?.getBoundingClientRect().bottom||0)
  }));
  if(scrollCheck.sectionTop<scrollCheck.headerBottom-2)fail.push("Anchor obscured by header");
  try{await page.screenshot({path:path.join(OUT,width+"-category.png"),timeout:12000,animations:"disabled"});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message.slice(0,120));}
  report.viewports.push({width,status:res.status(),...data,scrollCheck,initialConsent,brokenLinks,errors,networkFailures,fail});
  console.log("SERVICES_BROWSER_SUMMARY "+JSON.stringify({width,status:res.status(),h1:data.h1,gridColumns:data.gridColumns,cards:data.cards.length,workstreams:data.workstreamCount,statuses:data.scopeStatusCounts,groups:data.groupCount,choices:data.choiceCount,jumpLinks:data.jumpLinks.length,returnLinks:data.returnLinks,consent:initialConsent,consultGraphic:data.consultationGraphicCount,scrollCheck,footer:data.footerGeometry,overflow:data.scrollWidth>width,brokenLinks,errors,networkFailures,fail}));
  await ctx.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(OUT,"audit.json"),JSON.stringify(report,null,2));
 if(report.viewports.some(x=>x.fail.length))throw Error("EN services QA failed");
 console.log("SERVICES_BROWSER_PASS 390/768/1280 viewports, no broken links, no fake footer");
})().catch(async e=>{
 console.error("SERVICES_BROWSER_FATAL "+(e.stack||e));
 try{if(browser)await browser.close();}catch(closeError){console.error("SERVICES_BROWSER_CLOSE_WARNING "+closeError.message);}
 process.exitCode=1;
});
