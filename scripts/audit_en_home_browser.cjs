/* EN homepage visual and technical evidence: local Hugo output, 390px and 1280px. */
const fs=require("node:fs"), path=require("node:path");
const {chromium}=require("playwright");
const OUT="audit-artifacts/en-home", BASE="http://127.0.0.1:8765/";
fs.mkdirSync(OUT,{recursive:true});
(async()=>{
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const report={testedAt:new Date().toISOString(),url:BASE,viewports:[],notes:[
    "Lab browser of production-base Hugo HTML, not real-user Core Web Vitals.",
    "Screenshots at exact 390px and 1280px are saved to artifact."
  ]};
  for(const v of [390,1280]){
    const ctx=await browser.newContext({viewport:{width:v,height:v===390?844:800},
      isMobile:v===390,hasTouch:v===390,deviceScaleFactor:1,locale:"en-US"});
    const page=await ctx.newPage(),jsErrors=[],networkFailures=[];
    page.on("pageerror",e=>jsErrors.push(String(e.message).slice(0,180)));
    page.on("requestfailed",r=>networkFailures.push({url:r.url(),failure:r.failure()?.errorText}));
    console.log("AUDIT_STAGE "+v+" browser opened");
    await page.route("https://fonts.googleapis.com/**",route=>route.abort());
    await page.route("https://fonts.gstatic.com/**",route=>route.abort());
    const response=await page.goto(BASE,{waitUntil:"domcontentloaded",timeout:20000});
    console.log("AUDIT_STAGE "+v+" DOM loaded");
    await page.waitForTimeout(1100);
    const dom=await page.evaluate(()=>{
      const readMeta=q=>document.querySelector(q)?.getAttribute("content")||"";
      const box=q=>{let e=document.querySelector(q);if(!e)return null;
        let r=e.getBoundingClientRect();return {x:Math.round(r.x),y:Math.round(r.y),
          width:Math.round(r.width),height:Math.round(r.height)};};
      const imgs=Array.from(document.images).map(x=>({src:x.currentSrc,alt:x.getAttribute("alt"),
        loaded:x.complete&&x.naturalWidth>0,naturalWidth:x.naturalWidth}));
      const links=Array.from(document.querySelectorAll("a[href]")).map(x=>({
        href:x.href,label:(x.getAttribute("aria-label")||x.textContent||"").trim().slice(0,85)}));
      const schemas=Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(x=>{
        try{return {valid:true,rootType:JSON.parse(x.textContent)["@type"]||"graph"};}
        catch(e){return {valid:false,error:String(e).slice(0,140)};}
      });
      const banner=document.querySelector(".gdpr-consent-banner");
      const footer=document.querySelector(".custom-footer");
      const anchors=Array.from(document.querySelectorAll("a[href^='#']")).map(x=>{
        const href=x.getAttribute("href");
        if(!href || href==="#")return {href,targetExists:null,placeholder:true};
        let ok=false;
        try{ok=!!document.getElementById(decodeURIComponent(href.slice(1)));}
        catch(e){ok=false;}
        return {href,targetExists:ok};
      });
      return {title:document.title,lang:document.documentElement.lang,
        H1:Array.from(document.querySelectorAll("h1")).map(x=>x.innerText.trim()),
        headings:Array.from(document.querySelectorAll("h1,h2,h3")).map(x=>({
          tag:x.tagName,text:x.innerText.trim().slice(0,95)})),
        metaDescription:readMeta('meta[name="description"]'),
        canonical:document.querySelector('link[rel="canonical"]')?.href||"",
        robots:readMeta('meta[name="robots"]'),
        hreflang:Array.from(document.querySelectorAll('link[rel="alternate"][hreflang]')).map(x=>({
          lang:x.hreflang,href:x.href})),
        ogTitle:readMeta('meta[property="og:title"]'), ogDescription:readMeta('meta[property="og:description"]'),
        jsonLD:schemas,
        viewportWidth:innerWidth, scrollWidth:document.documentElement.scrollWidth,
        horizontalOverflow:document.documentElement.scrollWidth>innerWidth+2,
        documentHeight:document.documentElement.scrollHeight,
        hero:box(".seo-hero-panel"),process:box("#how-it-works"),cards:box(".seo-news-strip__side"),
        deliverables:box(".seo-en-home-deliverables"),cookie:box(".gdpr-consent-banner"),
        cookieVisible:!!banner&&getComputedStyle(banner).display!=="none",
        footer:box(".custom-footer"),
        footerPosition:footer?getComputedStyle(footer).position:null,
        images:imgs,links,anchors
      };
    });
    console.log("AUDIT_STAGE "+v+" DOM metrics collected");
    try{await page.screenshot({path:path.join(OUT,v+"-initial.png"),fullPage:false,timeout:12000,animations:"disabled"});}
    catch(e){console.log("AUDIT_SCREENSHOT_WARN "+v+" initial "+e.message.slice(0,130));}
    let cookieDismissed=false;
    try{const reject=page.getByRole("button",{name:/Reject Non-Essential/i});
      if(await reject.count()){await reject.first().click({timeout:4000});cookieDismissed=true;}}
    catch(e){jsErrors.push("Cookie dismissal: "+e.message.slice(0,120));}
    await page.waitForTimeout(400);
    console.log("AUDIT_STAGE "+v+" cookie evaluated "+cookieDismissed);
    try{await page.screenshot({path:path.join(OUT,v+"-full.png"),fullPage:true,timeout:12000,animations:"disabled"});}
    catch(e){console.log("AUDIT_SCREENSHOT_WARN "+v+" full "+e.message.slice(0,130));}
    await page.evaluate(()=>window.scrollTo(0,Math.max(0,document.documentElement.scrollHeight/2)));
    await page.waitForTimeout(450);
    const scroll=await page.evaluate(()=>({
      className:document.body.className,
      footerPosition:getComputedStyle(document.querySelector(".custom-footer")).position,
      footerRect:Math.round(document.querySelector(".custom-footer").getBoundingClientRect().top)
    }));
    await page.waitForTimeout(3500);
    const idle=await page.evaluate(()=>({
      className:document.body.className,
      footerPosition:getComputedStyle(document.querySelector(".custom-footer")).position,
      footerRect:Math.round(document.querySelector(".custom-footer").getBoundingClientRect().top)
    }));
    console.log("AUDIT_STAGE "+v+" scroll and idle tested");
    try{await page.screenshot({path:path.join(OUT,v+"-scrolled.png"),fullPage:false,timeout:12000,animations:"disabled"});}
    catch(e){console.log("AUDIT_SCREENSHOT_WARN "+v+" scroll "+e.message.slice(0,130));}
    const internal=[...new Set(dom.links.map(x=>x.href.split("#")[0]).filter(x=>x.startsWith(BASE)))];
    console.log("AUDIT_STAGE "+v+" checking "+internal.length+" internal paths");
    const brokenLinks=[];
    for(const href of internal){
      try{const r=await page.request.get(href,{timeout:12000});
        if(r.status()>=400)brokenLinks.push({href,status:r.status()});}
      catch(e){brokenLinks.push({href,error:e.message.slice(0,140)});}
    }
    const metrics={width:v,httpStatus:response.status(),...dom,cookieDismissed,
      scroll,afterIdle:idle,jsErrors,networkFailures,brokenLinks};
    report.viewports.push(metrics);
    console.log("AUDIT_STAGE "+v+" complete");
    console.log("HOME_QA_SUMMARY "+JSON.stringify({
      width:v,http:metrics.httpStatus,h1:dom.H1,canon:dom.canonical,title:dom.title,
      headings:dom.headings,overflow:dom.horizontalOverflow,scrollWidth:dom.scrollWidth,
      imgFailures:dom.images.filter(x=>!x.loaded),schemaErrors:dom.jsonLD.filter(x=>!x.valid),
      badAnchors:dom.anchors.filter(x=>!x.targetExists),
      brokenLinks,jsErrors,networkFailures,footerBefore:dom.footerPosition,
      afterScroll:scroll,afterIdle:idle,cookieDismissed
    }));
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT,"audit.json"),JSON.stringify(report,null,2));
  console.log("HOME_QA_FINISHED "+JSON.stringify({viewports:report.viewports.map(x=>x.width),
    hasOverflow:report.viewports.some(x=>x.horizontalOverflow),
    brokenImages:report.viewports.flatMap(x=>x.images.filter(z=>!z.loaded)).length,
    brokenLinks:report.viewports.flatMap(x=>x.brokenLinks).length}));
})().catch(e=>{console.error("HOME_QA_FATAL",e.stack||e);process.exitCode=1;});
