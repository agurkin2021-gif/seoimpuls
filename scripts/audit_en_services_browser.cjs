/* Audit both EN and RU seven-card homepages plus the four approved EN detail routes. */
const fs = require("node:fs"), path = require("node:path");
const {chromium} = require("playwright");
const ROOT = "http://127.0.0.1:8765";
const OUT = "audit-artifacts/en-services";
const TARGETS = [
  ["/technical-seo-audit/", "Technical SEO Audit"],
  ["/keyword-research/", "Keyword Research"],
  ["/seo-consultation/", "SEO Consultation"],
  ["/seo-retainer/", "SEO Retainer"],
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
      const cards=Array.from(document.querySelectorAll("#services article.seo-en-service-card"));
      const layout=document.getElementById("services");
      const meta=(name)=>document.querySelector('meta[name="'+name+'"]')?.content || "";
      const canonical=document.querySelector('link[rel="canonical"]')?.href||"";
      const images=Array.from(document.images).map(x=>({src:x.currentSrc,ok:x.complete&&x.naturalWidth>0}));
      return {
        title:document.title,h1:Array.from(document.querySelectorAll("h1")).map(x=>x.textContent.trim()),
        canonical,robots:meta("robots"),description:meta("description"),
        heroDesign:(()=>{
          const stage=document.querySelector(".seo-central--art-directed .seo-en-hero-stage");
          const copy=stage?.querySelector(".seo-en-hero-copy");
          const visual=stage?.querySelector(".seo-en-hero-visual");
          const rect=el=>{const r=el?.getBoundingClientRect();return r?{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}:null};
          return {stageCount:document.querySelectorAll(".seo-en-hero-stage").length,
            figureCount:document.querySelectorAll(".seo-en-hero-visual").length,
            svgCount:visual?.querySelectorAll("svg").length||0,
            aria:visual?.getAttribute("aria-label")||"",
            kicker:copy?.querySelector(".seo-en-hero-eyebrow")?.textContent.trim()||"",
            grid:stage?getComputedStyle(stage).gridTemplateColumns:"",
            copy:rect(copy),visual:rect(visual),stage:rect(stage),
            svgExternalImages:visual?.querySelectorAll("image, img, use[href^='http'], use[xlink\\:href^='http']").length||0};
        })(),
        cards:cards.map(x=>({
          href:x.querySelector("[data-home-service-link]")?.getAttribute("href")||"",
          kind:x.querySelector("[data-home-service-link]")?.dataset.homeServiceLink||"",
          id:x.dataset.homeService,title:x.querySelector("h3")?.textContent.trim()||"",featured:x.classList.contains("seo-en-service-card--featured"),
          summary:x.querySelector(".seo-en-service-card__head + p")?.textContent.trim()||"",
          outcome:x.querySelector(".seo-en-service-card__outcome")?.textContent.trim()||"",
          imageCount:x.querySelectorAll("img").length,
          mark:x.querySelector(".seo-en-service-mark")?.textContent.trim()||"",
          markRect:(()=>{const r=x.querySelector(".seo-en-service-mark")?.getBoundingClientRect();return r?{width:r.width,height:r.height}:null;})()
        })),
        columns:(()=>{const g=document.querySelector("#services .seo-en-primary-services__grid");return g?getComputedStyle(g).gridTemplateColumns.split(" ").filter(Boolean).length:0;})(),
        selectorCount:document.querySelectorAll("#seo-en-choose-title").length,
        scopeItems:document.querySelectorAll(".seo-central--en .seo-static-offer__list li").length,
        oldScopeIcon:!!document.querySelector('.seo-central--en img[src*="seo-icon-google.svg"]'),
        scopeHeading:document.querySelector(".seo-static-offer__title")?.textContent.trim()||"",
        serviceHeading:document.querySelector("#seo-en-services-title")?.textContent.trim()||"",
        projectAnchor:!!document.getElementById("contact-project"),
        processBelow:!!layout&&!!document.querySelector("#how-it-works")&&document.querySelector("#how-it-works").getBoundingClientRect().top>=layout.getBoundingClientRect().bottom-2,
        keywordDeliverable:document.querySelector(".seo-en-home-deliverables")?.textContent.includes("Keyword Research Spreadsheet")||false,
        independentKeyword:document.querySelector(".seo-en-home-scope")?.textContent.includes("For keyword research, no website is needed")||false,
        contactCTA:document.querySelector(".seo-en-home-scope-actions .seo-cta--primary")?.textContent.trim()||"",
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
    const hd=main.heroDesign;
    if(hd.stageCount!==1||hd.figureCount!==1||hd.svgCount!==1||!hd.aria.includes("search intent")||
       !hd.kicker.includes("TECHNICAL SEO")||hd.svgExternalImages)
      fail.push("EN first-screen diagram missing, inaccessible or using external image");
    if(!hd.copy||!hd.visual||!hd.stage||hd.stage.width<250||
       hd.visual.width<220||hd.visual.right>width+2||hd.visual.left<-2)
      fail.push("EN first-screen diagram outside visible viewport");
    if(hd.copy&&hd.visual){
      if(width>900&&hd.copy.right>hd.visual.left+3)fail.push("EN desktop hero copy overlaps diagram");
      if(width<=900&&hd.copy.bottom>hd.visual.top+3)fail.push("EN compact hero should stack copy above diagram");
    }
    if(main.cards.length!==7||main.selectorCount||!main.hasAnchor||main.serviceHeading!=="SEO Services for Your Business"||!main.projectAnchor)
      fail.push("Six merged SEO work areas plus featured SEO Retainer, heading or contact anchor missing");
    if(main.scopeItems!==0||main.oldScopeIcon||main.scopeHeading)
      fail.push("Legacy extra-work tiles still duplicate new primary services");
    const ids=["seo-audit","keyword-research","on-page-seo","local-seo","international-seo","seo-consultation","seo-retainer"];
    if(main.cards.map(x=>x.id).join("|")!==ids.join("|")||new Set(main.cards.map(x=>x.title)).size!==7)
      fail.push("Missing or duplicate commercial SEO service headings");
    if(!main.keywordDeliverable||!main.independentKeyword||main.contactCTA!=="Discuss Your SEO Project")
      fail.push("Buyer-facing keyword deliverable or business project CTA missing");
    const mergedEN=Object.fromEntries(main.cards.map(x=>[x.id,(x.summary+" "+x.outcome).toLowerCase()]));
    if(!["crawl","index","redirect","technical"].every(w=>mergedEN["seo-audit"]?.includes(w))||
       !["compet","topic","keyword"].every(w=>mergedEN["keyword-research"]?.includes(w))||
       !["content","heading","recommend"].every(w=>mergedEN["on-page-seo"]?.includes(w)))
      fail.push("Consolidated EN cards lost technical, competitor or page/content scope");
    if(main.cards.map(x=>x.mark).join("/")!=="01/02/03/04/05/06/07"||main.cards.some(x=>x.imageCount!==0||!x.markRect||x.markRect.width<36||Math.abs(x.markRect.width-x.markRect.height)>3))
      fail.push("Service design: seven lightweight CSS-only markers, no old image elements");
    if(main.cards.filter(x=>x.featured).length!==1||main.cards.at(-1).id!=="seo-retainer"||!main.cards.at(-1).featured)fail.push("Featured retainer must be the final service");
    for(const [url] of TARGETS)if(main.cards.filter(x=>x.href===url&&x.kind==="details").length!==1)fail.push("Missing one direct service detail link "+url);
    if(main.cards.filter(x=>x.kind==="contact"&&x.href==="#contact-project").length!==3)fail.push("Three scoped service enquiries do not reach contact anchor");
    if(main.serviceNav!=="/#services"||main.heroTarget!=="/#services")fail.push("Top services navigation/CTA not anchored");
    if(!main.faq)fail.push("Retained buyer FAQ missing");
    if(!main.processBelow)fail.push("Service cards should be visually above compact process");
    if(main.columns!==(width===390?1:width===768?2:3))fail.push("Responsive seven-card grid column count");
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
      const bounds=Array.from(document.querySelectorAll(".seo-central--en h1,.seo-central--en h2,.seo-central--en h3,.seo-central--en p,.seo-central--en li,.seo-central--en a"))
        .filter(x=>x.textContent.trim()&&getComputedStyle(x).display!=="none")
        .map(x=>({rect:x.getBoundingClientRect(),text:x.textContent.trim().slice(0,50)}));
      const floaters=Array.from(document.querySelectorAll(".footer-shortcut--whatsapp,.footer-shortcut--telegram"))
        .filter(x=>getComputedStyle(x).position==="fixed"&&x.getBoundingClientRect().width>0);
      const overlaps=[];
      for(const el of floaters)for(const item of bounds){const a=el.getBoundingClientRect(),b=item.rect;
        if(b.bottom>0&&b.top<innerHeight&&a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top)
          overlaps.push({button:el.className,buttonRect:[Math.round(a.left),Math.round(a.top),Math.round(a.right),Math.round(a.bottom)],textRect:[Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)],text:item.text});}
      return {sectionTop:Math.round(r.top),headerBottom:Math.round(h?.bottom||0),floatingCount:floaters.length,overlaps};
    });
    if(focus.sectionTop<focus.headerBottom-2)fail.push("Services anchor hidden by fixed header");
    if(focus.overlaps.length)fail.push("Floating contacts cover readable homepage text");
    await page.locator('a[data-home-link-field="heroBuilderUrl"]').focus();
    await page.keyboard.press("Enter");
    await page.waitForTimeout(130);
    const hash=await page.evaluate(()=>location.hash);
    if(hash!=="#services")fail.push("Keyboard Services CTA");
    if(errors.length||networkFailures.length)fail.push("JS or network failures");
    try{await page.screenshot({path:path.join(OUT,width+"-services.png"),animations:"disabled",timeout:12000});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message);}
    try{await page.screenshot({path:path.join(OUT,width+"-full.png"),fullPage:true,animations:"disabled",timeout:15000});}catch(e){console.log("SERVICES_SCREENSHOT_WARNING "+e.message);}

    // Check the actual new commercial page at each viewport; a correct homepage card is not enough.
    const retainerPage=await context.newPage();
    const retainerResponse=await retainerPage.goto(ROOT+"/seo-retainer/",{waitUntil:"domcontentloaded",timeout:25000});
    await retainerPage.waitForTimeout(150);
    const retainerVisual=await retainerPage.evaluate(()=>{
      const buttons=Array.from(document.querySelectorAll(".seo-builder-buttons a.seo-cta"))
        .map(a=>({label:a.textContent.trim(),href:a.getAttribute("href")}));
      return {
        title:document.title,
        h1:Array.from(document.querySelectorAll("h1")).map(x=>x.textContent.trim()),
        crumbs:Array.from(document.querySelectorAll(".breadcrumbs__item")).map(x=>x.textContent.trim()),
        buttons,
        sections:Array.from(document.querySelectorAll(".seo-builder-block[id]")).map(x=>x.id),
        missingTargets:buttons.filter(x=>x.href.includes("#")&&!document.getElementById(x.href.split("#")[1])),
        pageImages:document.querySelectorAll(".seo-builder img").length,
        overflow:document.documentElement.scrollWidth>innerWidth+2
      };
    });
    if(retainerResponse.status()!==200||retainerVisual.h1.length!==1||retainerVisual.h1[0]!=="SEO Retainer"||
       retainerVisual.title!=="SEO Retainer | SeoImpuls"||retainerVisual.crumbs.length!==2||
       retainerVisual.crumbs[1]!=="SEO Retainer"||retainerVisual.overflow||retainerVisual.pageImages)
      fail.push("Retainer page visual/H1/breadcrumb/overflow error");
    for(const id of ["overview","included","first-month","monthly-cycle","deliverables","scope","pricing","comparison","faq","start"])
      if(!retainerVisual.sections.includes(id))fail.push("Retainer missing section "+id);
    if(retainerVisual.missingTargets.length||!retainerVisual.buttons.some(x=>x.href==="/seo-retainer/#start")||
       !retainerVisual.buttons.some(x=>x.href==="/seo-retainer/#first-month"))
      fail.push("Retainer CTA routes or anchors invalid");
    try{await retainerPage.screenshot({path:path.join(OUT,width+"-retainer.png"),fullPage:true,animations:"disabled",timeout:16000});}
    catch(e){console.log("RETAINER_SCREENSHOT_WARNING "+e.message);}
    await retainerPage.close();
    // Same seven commercial choices must be visible and functional in RU working copy.
    const ruPage=await context.newPage(),ruErrors=[],ruNetworkFailures=[];
    ruPage.on("pageerror",e=>ruErrors.push(e.message));
    ruPage.on("requestfailed",r=>ruNetworkFailures.push({url:r.url(),reason:r.failure()?.errorText}));
    const ruResponse=await ruPage.goto(ROOT+"/ru/",{waitUntil:"domcontentloaded",timeout:25000});
    await ruPage.waitForTimeout(250);
    const ru=await ruPage.evaluate(()=>{
      const cards=Array.from(document.querySelectorAll("#services article.seo-en-service-card"));
      const grid=document.querySelector("#services .seo-en-primary-services__grid");
      return {
        lang:document.documentElement.lang,
        heroDiagramCount:document.querySelectorAll(".seo-en-hero-visual, .seo-en-hero-stage, .seo-central--art-directed").length,
        h1:Array.from(document.querySelectorAll("h1")).map(x=>x.textContent.trim()),
        ids:cards.map(x=>x.dataset.homeService),
        cards:cards.map(x=>({id:x.dataset.homeService,title:x.querySelector("h3")?.textContent.trim()||"",
          summary:x.querySelector(".seo-en-service-card__head + p")?.textContent.trim()||"",
          outcome:x.querySelector(".seo-en-service-card__outcome")?.textContent.trim()||"",
          route:x.querySelector("[data-home-service-link]")?.getAttribute("href")||"",
          kind:x.querySelector("[data-home-service-link]")?.dataset.homeServiceLink||"",
          mark:x.querySelector(".seo-en-service-mark")?.textContent.trim()||"",
          imageCount:x.querySelectorAll("img").length,featured:x.classList.contains("seo-en-service-card--featured")})),
        columns:grid?getComputedStyle(grid).gridTemplateColumns.split(" ").filter(Boolean).length:0,
        intro:document.querySelector(".seo-en-primary-services__intro")?.textContent.trim()||"",
        hasContact:!!document.getElementById("contact-project"),
        hasProcess:!!document.getElementById("how-it-works"),
        overflow:document.documentElement.scrollWidth>innerWidth+2,
        links:Array.from(document.querySelectorAll("a[href]")).map(x=>x.href)
      };
    });
    if(ru.heroDiagramCount!==0)fail.push("RU homepage unexpectedly received EN-only hero design");
    if(ruResponse.status()!==200||!ru.lang.toLowerCase().startsWith("ru")||
       ru.h1.length!==1||ru.h1[0]!=="Профессиональные SEO-услуги"||
       ru.ids.join("|")!==ids.join("|")||ru.cards.length!==7)
      fail.push("RU homepage seven-card H1, language or matching IDs");
    if(ru.cards.map(x=>x.mark).join("/")!=="01/02/03/04/05/06/07"||
       ru.cards.some(x=>x.imageCount)||ru.cards.filter(x=>x.featured).length!==1||
       !ru.cards.at(-1).featured||ru.columns!==(width===390?1:width===768?2:3))
      fail.push("RU numbered responsive card grid or featured retainer");
    for(const route of ["/ru/seo/","/ru/uslugi/semanticheskoe-yadro/","/ru/uslugi/seo-konsultaciya/"])
      if(ru.cards.filter(x=>x.kind==="details"&&x.route===route).length!==1)
        fail.push("Missing native RU service route "+route);
    if(ru.cards.filter(x=>x.kind==="contact"&&x.route==="/ru/#contact-project").length!==4)
      fail.push("Four RU enquiry cards must target RU contact anchor");
    const ruMerged=Object.fromEntries(ru.cards.map(x=>[x.id,(x.summary+" "+x.outcome).toLowerCase()]));
    if(!["индексац","перенаправлен"].every(x=>ruMerged["seo-audit"]?.includes(x))||
       !ruMerged["keyword-research"]?.includes("конкурент")||
       !["текст","заголовк"].every(x=>ruMerged["on-page-seo"]?.includes(x)))
      fail.push("RU audit/competitor/page-content merged coverage missing");
    if(!ru.hasContact||!ru.hasProcess||!ru.intro.includes("SEO-услуги для вашего бизнеса")||
       ru.overflow||ruErrors.length||ruNetworkFailures.length)
      fail.push("RU content/process/overflow or runtime issue");
    const ruPaths=Array.from(new Set(ru.links.filter(x=>x.startsWith(ROOT)).map(x=>new URL(x).pathname).filter(x=>x!=="/")));
    const ruBroken=[];
    for(const u of ruPaths){
      const file=path.join("public",decodeURIComponent(u).replace(/^[/]+/,""),u.endsWith("/")?"index.html":"");
      if(!fs.existsSync(file))ruBroken.push(u);
    }
    if(ruBroken.length)fail.push("Broken RU internal paths: "+ruBroken.join(", "));
    try{await ruPage.screenshot({path:path.join(OUT,width+"-ru-full.png"),fullPage:true,animations:"disabled",timeout:15000});}
    catch(e){console.log("RU_SCREENSHOT_WARNING "+e.message);}
    await ruPage.close();
    report.viewports.push({width,main,ru,ruBroken,ruErrors,ruNetworkFailures,children,focus,retainerVisual,broken,errors,networkFailures,fail});
    console.log("SERVICES_BROWSER_SUMMARY "+JSON.stringify({width,status:response.status(),cardCount:main.cards.length,
      serviceRoutes:main.cards.map(x=>x.href),ruCardCount:ru.cards.length,ruColumns:ru.columns,ruBroken,cardVisuals:main.cards.map(x=>({mark:x.mark,imageCount:x.imageCount,rect:x.markRect})),columns:main.columns,focus,errors,networkFailures,broken,retainerVisual,fail}));
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT,"audit.json"),JSON.stringify(report,null,2));
  if(report.viewports.some(x=>x.fail.length))throw Error("Direct EN services homepage QA failed");
  console.log("SERVICES_BROWSER_PASS: EN and RU both have 7 cards (six choices plus retainer), 3/2/1 responsive grid, four EN and three RU native detail routes at 390/768/1280");
})().catch(async e=>{
  console.error("SERVICES_BROWSER_FATAL "+(e.stack||e));
  try{if(browser)await browser.close()}catch(e){}
  process.exitCode=1;
});
