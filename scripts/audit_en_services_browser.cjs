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
    seoHead:(()=>{
      const meta=(name)=>document.querySelector('meta[name="'+name+'"]')?.content||document.querySelector('meta[property="'+name+'"]')?.content||"";
      return {lang:document.documentElement.lang,
        description:document.querySelector('meta[name="description" i]')?.content||"",
        robots:Array.from(document.querySelectorAll('meta[name="robots" i]')).map(x=>x.content),
        ogTitle:meta("og:title"),ogDescription:meta("og:description"),ogUrl:meta("og:url"),
        twitterCard:meta("twitter:card"),
        hreflang:Object.fromEntries(Array.from(document.querySelectorAll('link[rel="alternate"][hreflang]')).map(x=>[x.hreflang.toLowerCase(),x.href]))
      };
    })(),
    canonical:document.querySelector('link[rel="canonical"]')?.href||"",
    gridColumns:grid?getComputedStyle(grid).gridTemplateColumns.split(" ").filter(Boolean).length:0,
    workstreamCount:document.querySelectorAll(".seo-catalog__workstream").length,
    areaCount:document.querySelectorAll(".seo-catalog__area").length,
    topicCount:document.querySelectorAll(".seo-catalog__topic").length,
    scopeDisclaimer:(document.querySelector(".seo-catalog__scope-disclaimer")?.textContent||"").includes("These are not separate packages"),
    specialistQualifier:(document.querySelector(".seo-catalog__scope-disclaimer")?.textContent||"").includes("Additional work such as competitor research or page improvements"),
    choiceCount:document.querySelectorAll(".seo-catalog__choice").length,
    selectorBeforeCatalogue:(()=>{
      const selector=document.querySelector(".seo-catalog__matching");
      const heading=document.getElementById("seo-catalog-title");
      return !!selector&&!!heading&&!!(selector.compareDocumentPosition(heading)&Node.DOCUMENT_POSITION_FOLLOWING);
    })(),
    sampleLink:document.querySelector(".seo-catalog__sample-link")?.getAttribute("href")||"",
    catalogueScrollMargin:parseFloat(getComputedStyle(document.querySelector("#seo-catalog-title")).scrollMarginTop)||0,
    consultationGraphicCount:document.querySelectorAll(".services-hub-card__consult-visual").length,
    consultMediaImageCount:document.querySelectorAll('.services-hub-card[href$="/services/seo-consultation/"] img').length,
    reportExampleCount:document.querySelectorAll(".seo-catalog__evidence-item").length,
    verifiedInternalQaCount:document.querySelectorAll("[data-internal-qa-proof]").length,
    verifiedInternalQaLinks:Array.from(document.querySelectorAll('[data-internal-qa-proof] a[href]')).map(a=>a.href),
    exampleDisclaimer:(document.querySelector(".seo-catalog__example-note")?.textContent||"").includes("not a real client case"),
    faqQuestionCount:document.querySelectorAll(".seo-catalog__faq details").length,
    benefits:Array.from(document.querySelectorAll(".services-hub-card__benefit")).map(x=>x.textContent.trim()),
    keywordImagePresent:!!document.querySelector('img[src*="semantika-1788907052-q46-1788907068324.webp"]'),
    competitorExplained:(document.querySelector(".seo-catalog__areas")?.textContent||"").includes("SEO Competitor Analysis"),
    plainProcess:(document.querySelector(".seo-catalog__scope")?.textContent||"").includes("Tell us about your business"),
    detailLinks:Array.from(document.querySelectorAll(".seo-catalog__detail-link")).map(a=>({text:a.textContent.trim(),href:a.href})),
    legacyGranularEnquiries:document.querySelectorAll(".seo-catalog a[href^='mailto:'][href*='subject=']").length,
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
  if(data.h1.length!==1||data.h1[0]!=="Find the Right SEO Service for Your Business")fail.push("H1");
  if(data.title!=="SEO Audits, Keyword Research & Consulting | SeoImpuls")fail.push("Title");
  if(!/^(en-us|en)$/i.test(data.seoHead.lang)||data.seoHead.robots.length!==1||!data.seoHead.robots[0].startsWith("index,follow")||
     !data.seoHead.description.includes("Compare SEO audits")||!data.seoHead.ogTitle||!data.seoHead.ogDescription||
     !data.seoHead.ogUrl.endsWith("/seo-services/")||!data.seoHead.twitterCard)fail.push("SEO head metadata");
  for(const code of ["en-us","ru-ru","es-es","x-default"]){
     if(!data.seoHead.hreflang[code])fail.push("Missing hreflang "+code);
  }
  if(data.canonical!=="https://seoimpuls.com/seo-services/")fail.push("Canonical");
  if(data.cards.length!==3)fail.push("Cards");
  if(data.benefits.length!==3||!data.benefits.some(x=>x.includes("No website needed"))||!data.keywordImagePresent||!data.competitorExplained||!data.plainProcess)fail.push("Plain-language benefits or original keyword image missing");
  if(data.workstreamCount!==0||data.areaCount!==4||data.topicCount!==12||data.choiceCount!==3)fail.push("Concise four-area scope");
  if(!data.scopeDisclaimer||!data.specialistQualifier||data.legacyGranularEnquiries!==0||data.detailLinks.length)fail.push("Work components must not look like standalone offers");
  if(!data.selectorBeforeCatalogue)fail.push("Buyer choice must precede concise scope overview");
  if(data.sampleLink!=="#seo-catalog-example"||data.catalogueScrollMargin<100)fail.push("Useful report anchor");
  if(width===390 && initialConsent.shown && (initialConsent.layout!=="grid"||initialConsent.columns!==2||initialConsent.buttons!==3||!initialConsent.accept||!initialConsent.reject))fail.push("Mobile consent action layout");
  if(data.consultationGraphicCount!==1||data.consultMediaImageCount!==0)fail.push("Repeated consultation image");
  if(data.reportExampleCount!==4)fail.push("Evidence example");
  if(data.verifiedInternalQaCount!==1||data.verifiedInternalQaLinks.length!==2||
    !data.verifiedInternalQaLinks.some(x=>x.endsWith("/38851634798"))||
    !data.verifiedInternalQaLinks.some(x=>x.endsWith("/38851849354"))||!data.exampleDisclaimer)fail.push("Verifiable internal QA proof or honesty disclaimer");
  if(data.faqQuestionCount!==5)fail.push("Buyer FAQ coverage");
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

  // Keyboard navigation smoke checks; not a complete WCAG certification.
  const focusLink=page.locator(".seo-catalog__sample-link").first();
  await focusLink.focus();
  await page.keyboard.press("Enter");
  await page.waitForTimeout(180);
  const tocKeyboardHash=await page.evaluate(()=>location.hash);
  if(tocKeyboardHash!=="#seo-catalog-example")fail.push("Keyboard sample-report navigation");
  const faqSummary=page.locator(".seo-catalog__faq details summary").first();
  await faqSummary.focus();
  await page.keyboard.press("Enter");
  const faqOpened=await page.locator(".seo-catalog__faq details").first().evaluate(x=>x.open);
  if(!faqOpened)fail.push("Keyboard FAQ interaction");
  // A real hash jump must not place its section heading underneath the fixed header.
  await page.evaluate(()=>document.getElementById("seo-catalog-title").scrollIntoView({block:"start",behavior:"instant"}));
  await page.waitForTimeout(200);
  const scrollCheck=await page.evaluate(()=>({
    sectionTop:Math.round(document.getElementById("seo-catalog-title").getBoundingClientRect().top),
    headerBottom:Math.round(document.querySelector(".custom-header")?.getBoundingClientRect().bottom||0)
  }));
  // Visual regression: fixed social shortcuts must not cover readable catalogue text.
  const floatingContactOverlap=await page.evaluate(()=>{
    const isIntersect=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;
    const floated=[...document.querySelectorAll(".footer-shortcut--whatsapp,.footer-shortcut--telegram")]
      .filter(el=>getComputedStyle(el).position==="fixed" && el.getBoundingClientRect().width>0);
    const texts=[...document.querySelectorAll(".seo-catalog h2,.seo-catalog h3,.seo-catalog h4,.seo-catalog p,.seo-catalog li,.seo-catalog a")];
    const collisions=[];
    for(const button of floated){
      const b=button.getBoundingClientRect();
      for(const el of texts){
        const rect=el.getBoundingClientRect();
        if(rect.bottom<=0||rect.top>=innerHeight||rect.width===0||rect.height===0)continue;
        if(isIntersect(b,rect))collisions.push({button:button.className,text:el.textContent.trim().slice(0,65),buttonRight:Math.round(b.right),textLeft:Math.round(rect.left)});
      }
    }
    return {floatingIcons:floated.length,collisions};
  });
  if(width>=768&&floatingContactOverlap.collisions.length)fail.push("Floating contacts overlap catalogue text");
  if(scrollCheck.sectionTop<scrollCheck.headerBottom-2)fail.push("Anchor obscured by header");
  try{await page.screenshot({path:path.join(OUT,width+"-category.png"),timeout:12000,animations:"disabled"});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message.slice(0,120));}
  report.viewports.push({width,status:res.status(),...data,scrollCheck,initialConsent,brokenLinks,errors,networkFailures,fail});
  console.log("SERVICES_BROWSER_SUMMARY "+JSON.stringify({width,status:res.status(),h1:data.h1,seoHead:data.seoHead,faqOpened,keyboardTOC:tocKeyboardHash,gridColumns:data.gridColumns,cards:data.cards.length,oldWorkstreams:data.workstreamCount,areas:data.areaCount,topics:data.topicCount,granularEnquiries:data.legacyGranularEnquiries,choices:data.choiceCount,sampleLink:data.sampleLink,consent:initialConsent,consultGraphic:data.consultationGraphicCount,scrollCheck,footer:data.footerGeometry,floatingContactOverlap,overflow:data.scrollWidth>width,brokenLinks,errors,networkFailures,fail}));
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
