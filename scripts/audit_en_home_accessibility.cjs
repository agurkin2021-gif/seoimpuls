/* WCAG 2.2 automated checks for EN homepage at two CSS viewport sizes. */
const fs=require("node:fs"),path=require("node:path");
const {chromium}=require("playwright");
const axePath=require.resolve("axe-core/axe.min.js");
const BASE="http://127.0.0.1:8765/";
const OUT="audit-artifacts/en-home-accessibility";
fs.mkdirSync(OUT,{recursive:true});
function label(el) {
  return (el?.getAttribute("aria-label")||el?.getAttribute("title")||
    el?.innerText||el?.textContent||"").trim().slice(0,90);
}
(async()=>{
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const result={base:BASE,generatedAt:new Date().toISOString(),viewports:[],
    limits:["Automated axe WCAG checks do not certify WCAG conformance.",
      "Chromium local Hugo production-base build; browser settings and live SEO traffic not measured.",
      "Focus indicators need visual human verification even if outline information is collected."]};
  for(const width of [390,1280]){
    console.log("ACCESSIBILITY_STAGE "+width+" starting");
    const context=await browser.newContext({viewport:{width,height:width===390?844:800},
      isMobile:width===390,hasTouch:width===390,deviceScaleFactor:1,
      locale:"en-US",reducedMotion:"reduce"});
    const page=await context.newPage();
    await page.goto(BASE,{waitUntil:"domcontentloaded",timeout:25000});
    await page.waitForTimeout(500);
    const cookie=page.getByRole("button",{name:/Reject Non-Essential/i});
    if(await cookie.count()) await cookie.first().click({timeout:5000});
    await page.waitForTimeout(250);
    await page.addScriptTag({path:axePath});
    const data=await page.evaluate(async()=>{
      const report=await window.axe.run(document,{
        runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa"]}
      });
      return {
        violations:report.violations.map(v=>({
          id:v.id,impact:v.impact,description:v.help,helpUrl:v.helpUrl,
          nodes:v.nodes.map(n=>({
            target:n.target,html:n.html?.slice(0,250),
            failureSummary:n.failureSummary?.slice(0,480),
            any:n.any.map(check=>({id:check.id,message:check.message?.slice(0,380),data:check.data}))
          })).slice(0,30)
        })),
        incomplete:report.incomplete.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length})),
        passes:report.passes.map(v=>v.id),
        inapplicable:report.inapplicable.map(v=>v.id)
      };
    });
    // Also test the existing light theme, while leaving all user settings untouched.
    await page.evaluate(()=>document.body.setAttribute("theme","light"));
    await page.waitForTimeout(200);
    const light=await page.evaluate(async()=>{
      const r=await window.axe.run(document,{
        runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa"]}
      });
      return {
        violations:r.violations.map(v=>({id:v.id,impact:v.impact,
          nodes:v.nodes.map(n=>({target:n.target,html:n.html?.slice(0,240),
            failureSummary:n.failureSummary?.slice(0,470)})).slice(0,30)})),
        incomplete:r.incomplete.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length}))
      };
    });
    console.log("ACCESSIBILITY_LIGHT_SUMMARY "+JSON.stringify({
      width,violations:light.violations.map(v=>({id:v.id,impact:v.impact,
        targets:v.nodes.map(n=>n.target),nodes:v.nodes.length})),incomplete:light.incomplete
    }));
    await page.evaluate(()=>document.body.setAttribute("theme","dark"));
    // Keyboard navigation is inspected without claiming success from the mere presence of CSS.
    await page.evaluate(()=>{document.activeElement?.blur(); window.scrollTo(0,0);});
    const focus=[];
    for(let i=0;i<35;i++){
      await page.keyboard.press("Tab");
      const curr=await page.evaluate(()=>{
        const e=document.activeElement;
        if(!e || e===document.body)return null;
        const st=getComputedStyle(e),r=e.getBoundingClientRect();
        const name=(e.getAttribute("aria-label")||e.getAttribute("title")||e.textContent||"").trim().slice(0,100);
        return {tag:e.tagName,role:e.getAttribute("role"),name,
          id:e.id,href:e.getAttribute("href"),outlineWidth:st.outlineWidth,
          outlineStyle:st.outlineStyle,outlineColor:st.outlineColor,
          boxShadow:st.boxShadow,visible:r.width>0&&r.height>0,
          bounds:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}
        };
      });
      if(curr)focus.push(curr);
    }
    const widthResults={width,violations:data.violations,incomplete:data.incomplete,
      lightTheme:light,passedRules:data.passes.length,inapplicableRules:data.inapplicable.length,
      keyboardSample:focus};
    result.viewports.push(widthResults);
    console.log("ACCESSIBILITY_SUMMARY "+JSON.stringify({
      width,violations:data.violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target).slice(0,8),nodes:v.nodes.length})),
      incomplete:data.incomplete.slice(0,12),tabs:focus.length,firstTabs:focus.slice(0,8).map(x=>({name:x.name,id:x.id,outline:x.outlineWidth,style:x.outlineStyle}))
    }));
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT,"accessibility.json"),JSON.stringify(result,null,2));
  console.log("ACCESSIBILITY_FINISHED "+JSON.stringify({
    viewports:result.viewports.map(x=>x.width),
    totalViolations:result.viewports.reduce((n,x)=>n+x.violations.length,0)
  }));
  const confirmed=result.viewports.flatMap(v=>[
    ...v.violations.map(x=>({theme:"dark",width:v.width,id:x.id,impact:x.impact})),
    ...v.lightTheme.violations.map(x=>({theme:"light",width:v.width,id:x.id,impact:x.impact}))
  ]);
  const critical=confirmed.filter(x=>x.impact==="serious" || x.impact==="critical");
  if(critical.length){
    console.error("ACCESSIBILITY_GATE_FAIL "+JSON.stringify(critical));
    process.exitCode=1;
  } else {
    console.log("ACCESSIBILITY_GATE_PASS no serious/critical automated violations");
  }
  const focus=result.viewports.flatMap(v=>v.keyboardSample.filter(x=>["Explore SEO Services","Discuss Your Project","Discuss Your SEO Project"].includes(x.name))
    .map(x=>({width:v.width,name:x.name,style:x.outlineStyle,widthOutline:x.outlineWidth})));
  const missingFocus=focus.filter(x=>x.style==="none" || parseFloat(x.widthOutline||0)<2);
  if(missingFocus.length){
    console.error("EN_CTA_FOCUS_GATE_FAIL "+JSON.stringify(missingFocus.slice(0,10)));
    process.exitCode=1;
  }else console.log("EN_CTA_FOCUS_GATE_PASS "+focus.length+" focus states");

})().catch(e=>{console.error("ACCESSIBILITY_FATAL",e.stack||e);process.exitCode=1;});
