/* EN homepage services selection and three exact commercial service routes. */
const fs = require("node:fs"), path = require("node:path");
const {chromium} = require("playwright");
const ROOT = "http://127.0.0.1:8765";
const OUT = "audit-artifacts/en-services";
const TARGETS = [
  ["/technical-seo-audit/", "Technical SEO Audit"],
  ["/keyword-research/", "Keyword Research"],
  ["/seo-consultation/", "SEO Consultation"],
];
fs.mkdirSync(OUT,{recursive:true});
let browser;
(async()=>{
  browser = await chromium.launch({headless:true,args:["--no-sandbox"]});
  const report = {root:ROOT,viewports:[]};
  for(const width of [390,768,1280]){
    const context=await browser.newContext({
      viewport:{width,height:width===390?844:800},deviceScaleFactor:1,
      isMobile:width===390,hasTouch:width===390,locale:"en-US",reducedMotion:"reduce"
    });
    const page=await context.newPage(),errors=[],networkFailures=[];
    page.on("pageerror",e=>errors.push(e.message));
    page.on("requestfailed",r=>networkFailures.push({url:r.url(),reason:r.failure()?.errorText}));
    const response=await page.goto(ROOT+"/",{waitUntil:"domcontentloaded",timeout:25000});
    await page.waitForTimeout(500);
    try{await page.screenshot({path:path.join(OUT,width+"-initial.png"),animations:"disabled",timeout:12000});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message);}
    const reject=page.getByRole("button",{name:/Reject Non-Essential/i});
    if(await reject.count())await reject.first().click({timeout:5000});
    await page.evaluate(()=>document.querySelectorAll("img[loading=lazy]").forEach(x=>x.loading="eager"));
    await page.waitForTimeout(300);
    const main=await page.evaluate(()=>{
      const cards=Array.from(document.querySelectorAll("#services a.seo-card"));
      const layout=document.getElementById("services");
      const meta=(name)=>document.querySelector('meta[name="'+name+'"]')?.content || "";
      const canonical=document.querySelector('link[rel="canonical"]')?.href||"";
      const images=Array.from(document.images).map(x=>({src:x.currentSrc,ok:x.complete&&x.naturalWidth>0}));
      return {
        title:document.title,h1:Array.from(document.querySelectorAll("h1")).map(x=>x.textContent.trim()),
        canonical,robots:meta("robots"),description:meta("description"),
        cards:cards.map(x=>({href:new URL(x.href).pathname,label:x.textContent.trim()})),
        columns:layout?getComputedStyle(layout).gridTemplateColumns.split(" ").filter(Boolean).length:0,
        selectorCount:document.querySelectorAll("#seo-en-choose-title").length,
        heroTarget:document.querySelector('[data-home-link-field="heroBuilderUrl"]')?.getAttribute("href")||"",
        serviceNav:Array.from(document.querySelectorAll("nav.custom-header__nav a")).find(x=>x.textContent.trim()==="Services")?.getAttribute("href")||"",
        hasAnchor:!!layout,faq:!!document.getElementById("seo-en-buyer-faq-title"),
        schema:Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(x=>{try{return JSON.parse(x.textContent)["@type"]}catch(e){return "INVALID"}}),
        links:Array.from(document.querySelectorAll("a[href]")).map(x=>x.href),
        images,overflow:document.documentElement.scrollWidth>innerWidth+2,
      };
    });
    const fail=[];
    if(response.status()!==200)fail.push("Home HTTP "+response.status());
    if(main.title!=="Professional SEO Services | SeoImpuls")fail.push("Home title "+main.title);
    if(main.h1.length!==1||main.h1[0]!=="Professional SEO Services")fail.push("Home H1");
    if(main.canonical!=="https://seoimpuls.com/")fail.push("Home canonical");
    if(main.cards.length!==3||main.selectorCount||!main.hasAnchor)fail.push("Three primary direct services without duplicate selection");
    for(const [url] of TARGETS)if(main.cards.filter(x=>x.href===url).length!==1)fail.push("Missing one direct service "+url);
    if(main.serviceNav!=="/#services"||main.heroTarget!=="/#services")fail.push("Top services navigation/CTA not anchored");
    if(!main.faq)fail.push("Retained buyer FAQ missing");
    if(main.overflow)fail.push("Horizontal overflow");
    if(main.images.some(x=>!x.ok))fail.push("Broken home images");
    if(main.schema.includes("INVALID")||!main.schema.includes("WebSite")||!main.schema.includes("Organization"))fail.push("Home structured data");
    const paths=Array.from(new Set(main.links.filter(x=>x.startsWith(ROOT)).map(x=>new URL(x).pathname).filter(x=>x!=="/")));
    const broken=[];
    for(const p of paths) {
      const candidate=path.join("public",decodeURIComponent(p).replace(/^\/+/,""),p.endsWith("/")?"index.html":"");
      if(!fs.existsSync(candidate))broken.push({path:p,file:candidate});
    }
    if(broken.length)fail.push("Broken internal links");
    const children=[];
    for(const [url,name] of TARGETS){
      const detail=await page.request.get(ROOT+url,{timeout:15000});
      if(detail.status()!==200){fail.push("Service HTTP "+url+" "+detail.status());continue;}
      const html=await detail.text();
      const doc=await page.evaluate((source)=>{
        const p=new DOMParser().parseFromString(source,"text/html");
        const schemas=Array.from(p.querySelectorAll('script[type="application/ld+json"]')).map(x=>{try{return JSON.parse(x.textContent)["@type"]}catch(e){return "INVALID"}});
        return {h1:Array.from(p.querySelectorAll("h1")).map(x=>x.textContent.trim()),title:p.title,
          canonical:p.querySelector('link[rel="canonical"]')?.href||"",schemas,
          bodyWords:p.body.textContent.length};
      },html);
      children.push({url,name,...doc});
      if(doc.h1.length!==1||doc.h1[0]!==name||doc.title!==name+" | SeoImpuls"||
         doc.canonical!=="https://seoimpuls.com"+url||!doc.schemas.includes("WebPage")||
         !doc.schemas.includes("BreadcrumbList")||doc.schemas.includes("BlogPosting"))fail.push("Bad service SEO "+url);
    }
    for(const old of ["/seo/","/seo-services/","/services/","/services/keyword-research/","/services/seo-consultation/"]){
      if(fs.existsSync(path.join("public",old.slice(1),"index.html")))fail.push("Retired EN URL still generated "+old);
    }
    await page.evaluate(()=>document.getElementById("services").scrollIntoView({block:"start",behavior:"instant"}));
    await page.waitForTimeout(150);
    const focus=await page.evaluate(()=>{
      const section=document.getElementById("services"),header=document.querySelector(".custom-header");
      const r=section.getBoundingClientRect(),h=header?.getBoundingClientRect();
      const bounds=Array.from(section.querySelectorAll(".seo-card h3,.seo-card li")).map(x=>x.getBoundingClientRect());
      const floaters=Array.from(document.querySelectorAll(".footer-shortcut--whatsapp,.footer-shortcut--telegram"))
        .filter(x=>getComputedStyle(x).position==="fixed"&&x.getBoundingClientRect().width>0);
      const overlaps=[];
      for(const el of floaters)for(const b of bounds){const a=el.getBoundingClientRect();
        if(b.bottom>0&&b.top<innerHeight&&a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top)overlaps.push(el.className);}
      return {sectionTop:Math.round(r.top),headerBottom:Math.round(h?.bottom||0),floatingCount:floaters.length,overlaps};
    });
    if(focus.sectionTop<focus.headerBottom-2)fail.push("Services anchor hidden by fixed header");
    if(focus.overlaps.length)fail.push("Floating contacts cover readable service cards");
    await page.locator('a[data-home-link-field="heroBuilderUrl"]').focus();
    await page.keyboard.press("Enter");
    await page.waitForTimeout(130);
    const hash=await page.evaluate(()=>location.hash);
    if(hash!=="#services")fail.push("Keyboard Services CTA");
    if(errors.length||networkFailures.length)fail.push("JS or network failures");
    try{await page.screenshot({path:path.join(OUT,width+"-services.png"),animations:"disabled",timeout:12000});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message);}
    try{await page.screenshot({path:path.join(OUT,width+"-full.png"),fullPage:true,animations:"disabled",timeout:15000});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message);}
    report.viewports.push({width,main,children,focus,broken,errors,networkFailures,fail});
    console.log("SERVICES_BROWSER_SUMMARY "+JSON.stringify({width,status:response.status(),cardCount:main.cards.length,
      serviceRoutes:main.cards.map(x=>x.href),columns:main.columns,focus,errors,networkFailures,broken,fail}));
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT,"audit.json"),JSON.stringify(report,null,2));
  if(report.viewports.some(x=>x.fail.length))throw Error("Direct EN services homepage QA failed");
  console.log("SERVICES_BROWSER_PASS: homepage 3 direct exact-intent services at 390/768/1280, no obsolete catalog");
})().catch(async e=>{
  console.error("SERVICES_BROWSER_FATAL "+(e.stack||e));
  try{if(browser)await browser.close()}catch(e){}
  process.exitCode=1;
});
