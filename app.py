import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Image Template Generator",
    page_icon="🖼️",
    layout="wide",
)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
body{margin:0;background:#f7f7f8;color:#18181b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.app{width:100%;min-height:760px}
.layout{display:grid;grid-template-columns:340px minmax(0,1fr);min-height:760px;background:white;border:1px solid #e4e4e7;border-radius:14px;overflow:hidden}
.sidebar{padding:22px;border-right:1px solid #e4e4e7;background:white;overflow-y:auto}
.title{font-size:20px;font-weight:700;margin-bottom:5px}.subtitle{font-size:13px;color:#71717a;margin-bottom:22px}
.section{margin-bottom:18px}.section-title{font-size:13px;font-weight:700;margin-bottom:9px}.divider{height:1px;background:#e4e4e7;margin:20px 0}
.file-input{width:100%;padding:8px;border:1px solid #d4d4d8;border-radius:8px;background:white;font-size:13px}
.label{display:block;font-size:12px;color:#52525b;margin-bottom:5px}
.input{width:100%;padding:9px 10px;border:1px solid #d4d4d8;border-radius:8px;background:white;outline:none}
.input:focus{border-color:#18181b;box-shadow:0 0 0 2px #e4e4e7}.select{width:100%;padding:9px 10px;border:1px solid #d4d4d8;border-radius:8px;background:white}
.button{width:100%;padding:10px 12px;border-radius:9px;cursor:pointer;font-weight:600;border:1px solid #d4d4d8;background:white}
.button:hover{background:#f4f4f5}.button-primary{background:#18181b;color:white;border-color:#18181b}.button-primary:hover{background:#27272a}.button:disabled{opacity:.45;cursor:not-allowed}
.field{padding:14px 0;border-bottom:1px solid #eeeeef}.field-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}.field-number{font-size:12px;font-weight:700;color:#52525b}
.remove-button{border:none;background:transparent;color:#a1a1aa;cursor:pointer;font-size:12px}.remove-button:hover{color:#dc2626}.field-settings{margin-top:10px}
.inline{display:grid;grid-template-columns:1fr 1fr;gap:8px}.photo-status{margin-top:8px;padding:9px;border-radius:8px;background:#f4f4f5;font-size:12px;color:#52525b}
.preview-panel{min-width:0;display:flex;flex-direction:column;background:#fafafa}.preview-header{padding:18px 22px;border-bottom:1px solid #e4e4e7;background:white}
.preview-title{font-size:16px;font-weight:700}.preview-help{margin-top:3px;font-size:12px;color:#71717a}
.preview-area{flex:1;min-height:650px;display:flex;align-items:center;justify-content:center;padding:25px;overflow:auto}
.empty-preview{text-align:center;color:#71717a}.empty-icon{font-size:42px;margin-bottom:8px}
.canvas-container{position:relative;display:inline-block;line-height:0;user-select:none;background:white;box-shadow:0 8px 30px rgba(0,0,0,.08)}
.canvas-container>img{display:block;max-width:100%;max-height:650px;width:auto;height:auto}
.text-element{position:absolute;line-height:1.15;white-space:nowrap;cursor:grab;user-select:none;padding:4px 6px;border:1px dashed transparent}
.text-element:hover{border-color:#71717a;background:rgba(255,255,255,.15)}.text-element.selected{border-color:#18181b;background:rgba(255,255,255,.2)}.text-element.dragging{cursor:grabbing}
.photo-element{position:absolute;cursor:grab;border:1px dashed transparent;user-select:none;line-height:0}.photo-element:hover{border-color:#71717a}.photo-element.selected{border:1px dashed #18181b}.photo-element.dragging{cursor:grabbing}
.photo-element img{display:block;width:100%;height:100%;object-fit:contain;pointer-events:none}
.resize-handle{position:absolute;width:13px;height:13px;right:-7px;bottom:-7px;border:1px solid #18181b;background:white;border-radius:3px;cursor:nwse-resize}
.status{margin-top:8px;padding:9px;border-radius:8px;background:#f4f4f5;color:#52525b;font-size:12px;line-height:1.5}.status.success{background:#ecfdf5;color:#166534}.status.error{background:#fef2f2;color:#991b1b}
.size-row{display:grid;grid-template-columns:1fr 100px;gap:8px}
@media(max-width:850px){.layout{grid-template-columns:1fr}.sidebar{border-right:none;border-bottom:1px solid #e4e4e7}.preview-area{min-height:500px}}
</style>
</head>
<body>
<div class="app"><div class="layout">
<aside class="sidebar">
<div class="title">Image Template Generator</div>
<div class="subtitle">Create synthetic test images from any template.</div>

<div class="section">
<div class="section-title">1. Select Template</div>
<input id="templateInput" class="file-input" type="file" accept="image/png,image/jpeg,image/webp">
</div>

<div class="divider"></div>

<div class="section">
<div class="section-title">2. Fields</div>
<div id="fields"></div>
<button id="addFieldButton" class="button" type="button">+ Add Field</button>
</div>

<div class="divider"></div>

<div class="section">
<div class="section-title">3. Photo</div>
<input id="photoInput" class="file-input" type="file" accept="image/png,image/jpeg,image/webp">
<div id="photoStatus" class="photo-status" style="display:none"></div>
<button id="removePhotoButton" class="button" type="button" style="display:none;margin-top:8px">Remove Photo</button>
</div>

<div class="divider"></div>

<div class="section">
<div class="section-title">4. Bulk Generation</div>
<button id="csvButton" class="button" type="button">Upload CSV</button>
<input id="csvInput" type="file" accept=".csv,text/csv" style="display:none">
<div id="csvStatus" class="status" style="display:none"></div>
</div>

<div class="divider"></div>

<div class="section">
<div class="section-title">5. Download Settings</div>
<label class="label">Format</label>
<select id="formatInput" class="select">
<option value="jpeg">JPEG</option><option value="png">PNG</option><option value="webp">WebP</option>
</select>
<div style="height:10px"></div>
<label class="label">Size Mode</label>
<select id="sizeMode" class="select">
<option value="none">Original / No Size Limit</option><option value="maximum">Maximum Size</option><option value="target">Target Size</option>
</select>
<div style="height:10px"></div>
<div class="size-row">
<input id="sizeValue" class="input" type="number" min="1" value="100">
<select id="sizeUnit" class="select"><option value="KB">KB</option><option value="MB">MB</option></select>
</div>
</div>

<div class="divider"></div>

<div class="section">
<div class="section-title">6. Generate</div>
<button id="downloadButton" class="button button-primary" type="button" disabled>Download Image</button>
<button id="downloadZipButton" class="button button-primary" type="button" disabled style="display:none;margin-top:8px">Generate & Download ZIP</button>
<div id="generationStatus" class="status" style="display:none"></div>
</div>
</aside>

<section class="preview-panel">
<div class="preview-header">
<div class="preview-title">Live Preview</div>
<div class="preview-help">Drag text and photo elements directly on the template. Drag the corner of the photo to resize it.</div>
</div>
<div id="previewArea" class="preview-area">
<div class="empty-preview"><div class="empty-icon">🖼️</div><div>Select a template to begin.</div></div>
</div>
</section>
</div></div>

<script type="module">
import JSZip from "https://cdn.jsdelivr.net/npm/jszip@3.10.1/+esm";

const state={templateDataUrl:null,templateImage:null,photoDataUrl:null,photoImage:null,photoX:65,photoY:30,photoWidth:22,fields:[],csvRows:[],csvHeaders:[],selectedId:null,selectedType:null};

const templateInput=document.getElementById("templateInput");
const photoInput=document.getElementById("photoInput");
const fieldsContainer=document.getElementById("fields");
const previewArea=document.getElementById("previewArea");
const addFieldButton=document.getElementById("addFieldButton");
const photoStatus=document.getElementById("photoStatus");
const removePhotoButton=document.getElementById("removePhotoButton");
const csvButton=document.getElementById("csvButton");
const csvInput=document.getElementById("csvInput");
const csvStatus=document.getElementById("csvStatus");
const formatInput=document.getElementById("formatInput");
const sizeMode=document.getElementById("sizeMode");
const sizeValue=document.getElementById("sizeValue");
const sizeUnit=document.getElementById("sizeUnit");
const downloadButton=document.getElementById("downloadButton");
const downloadZipButton=document.getElementById("downloadZipButton");
const generationStatus=document.getElementById("generationStatus");

function createId(){return Date.now().toString(36)+Math.random().toString(36).substring(2)}
function getField(id){return state.fields.find(f=>f.id===id)}
function escapeHtml(value){return String(value??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;")}
function bytesFromSize(){const value=Number(sizeValue.value);if(!Number.isFinite(value)||value<=0)return null;return sizeUnit.value==="MB"?value*1024*1024:value*1024}
function showStatus(element,message,type=""){element.style.display="block";element.className="status "+type;element.innerHTML=message}

templateInput.addEventListener("change",event=>{
 const file=event.target.files?.[0]; if(!file)return;
 const reader=new FileReader();
 reader.onload=()=>{
  state.templateDataUrl=reader.result;
  const image=new Image();
  image.onload=()=>{state.templateImage=image;downloadButton.disabled=false;renderPreview()};
  image.src=state.templateDataUrl;
 };
 reader.readAsDataURL(file);
});

photoInput.addEventListener("change",event=>{
 const file=event.target.files?.[0]; if(!file)return;
 const reader=new FileReader();
 reader.onload=()=>{
  state.photoDataUrl=reader.result;
  const image=new Image();
  image.onload=()=>{
   state.photoImage=image;
   photoStatus.style.display="block";
   photoStatus.innerHTML="Photo loaded. Drag and resize it on the preview.";
   removePhotoButton.style.display="block";
   renderPreview();
  };
  image.src=state.photoDataUrl;
 };
 reader.readAsDataURL(file);
});

removePhotoButton.addEventListener("click",()=>{
 state.photoDataUrl=null;state.photoImage=null;photoInput.value="";photoStatus.style.display="none";removePhotoButton.style.display="none";renderPreview();
});

function addField(heading="",value=""){
 const field={id:createId(),heading:heading||`Field ${state.fields.length+1}`,value,x:50,y:50,fontSize:28,fontFamily:"Arial",fontWeight:"normal",color:"#000000"};
 state.fields.push(field);state.selectedId=field.id;state.selectedType="text";renderFields();renderPreview();
}
function removeField(id){
 state.fields=state.fields.filter(field=>field.id!==id);
 if(state.selectedId===id){state.selectedId=null;state.selectedType=null}
 renderFields();renderPreview();
}
function renderFields(){
 fieldsContainer.innerHTML="";
 if(state.fields.length===0){
  const empty=document.createElement("div");empty.style.fontSize="12px";empty.style.color="#71717a";empty.style.marginBottom="12px";empty.textContent="No fields yet. Click + Add Field.";fieldsContainer.appendChild(empty);
 }
 state.fields.forEach((field,index)=>{
  const wrapper=document.createElement("div");wrapper.className="field";
  wrapper.innerHTML=`
   <div class="field-header"><span class="field-number">Field ${index+1}</span><button type="button" class="remove-button" data-remove="${field.id}">Remove</button></div>
   <label class="label">Heading</label>
   <input class="input" data-heading="${field.id}" value="${escapeHtml(field.heading)}" placeholder="e.g. Name">
   <label class="label" style="margin-top:10px">Value</label>
   <input class="input" data-value="${field.id}" value="${escapeHtml(field.value)}" placeholder="e.g. Rahul">
   <div class="field-settings">
    <div class="inline">
     <div><label class="label">Font Size</label><input class="input" type="number" min="6" max="200" data-font="${field.id}" value="${field.fontSize}"></div>
     <div><label class="label">Color</label><input class="input" type="color" data-color="${field.id}" value="${field.color}" style="height:39px;padding:3px"></div>
    </div>
    <div style="margin-top:8px"><label class="label">Font</label><select class="select" data-font-family="${field.id}">
     <option value="Arial" ${field.fontFamily==="Arial"?"selected":""}>Arial</option>
     <option value="Verdana" ${field.fontFamily==="Verdana"?"selected":""}>Verdana</option>
     <option value="Georgia" ${field.fontFamily==="Georgia"?"selected":""}>Georgia</option>
     <option value="Times New Roman" ${field.fontFamily==="Times New Roman"?"selected":""}>Times New Roman</option>
    </select></div>
    <div style="margin-top:8px"><label class="label">Weight</label><select class="select" data-font-weight="${field.id}">
     <option value="normal" ${field.fontWeight==="normal"?"selected":""}>Normal</option>
     <option value="bold" ${field.fontWeight==="bold"?"selected":""}>Bold</option>
    </select></div>
   </div>`;
  fieldsContainer.appendChild(wrapper);
 });
 fieldsContainer.querySelectorAll("[data-heading]").forEach(input=>input.addEventListener("input",e=>{const f=getField(e.target.dataset.heading);if(f){f.heading=e.target.value;renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-value]").forEach(input=>input.addEventListener("input",e=>{const f=getField(e.target.dataset.value);if(f){f.value=e.target.value;renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-font]").forEach(input=>input.addEventListener("input",e=>{const f=getField(e.target.dataset.font);if(f){f.fontSize=Math.max(6,Math.min(200,Number(e.target.value)));renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-color]").forEach(input=>input.addEventListener("input",e=>{const f=getField(e.target.dataset.color);if(f){f.color=e.target.value;renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-font-family]").forEach(input=>input.addEventListener("change",e=>{const f=getField(e.target.dataset.fontFamily);if(f){f.fontFamily=e.target.value;renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-font-weight]").forEach(input=>input.addEventListener("change",e=>{const f=getField(e.target.dataset.fontWeight);if(f){f.fontWeight=e.target.value;renderPreview()}}));
 fieldsContainer.querySelectorAll("[data-remove]").forEach(button=>button.addEventListener("click",()=>removeField(button.dataset.remove)));
}
addFieldButton.addEventListener("click",()=>addField());

function renderPreview(){
 previewArea.innerHTML="";
 if(!state.templateImage){
  previewArea.innerHTML='<div class="empty-preview"><div class="empty-icon">🖼️</div><div>Select a template to begin.</div></div>';return;
 }
 const container=document.createElement("div");container.className="canvas-container";
 const image=document.createElement("img");image.src=state.templateDataUrl;image.alt="Template";container.appendChild(image);

 state.fields.forEach(field=>{
  const element=document.createElement("div");element.className="text-element";
  if(state.selectedId===field.id&&state.selectedType==="text")element.classList.add("selected");
  element.textContent=field.value||`{{${field.heading||"FIELD"}}}`;
  element.style.left=`${field.x}%`;element.style.top=`${field.y}%`;element.style.fontSize=`${field.fontSize}px`;element.style.fontFamily=field.fontFamily;element.style.fontWeight=field.fontWeight;element.style.color=field.color;
  container.appendChild(element);enableTextDragging(element,container,field);
 });

 if(state.photoDataUrl&&state.photoImage){
  const photo=document.createElement("div");photo.className="photo-element";
  if(state.selectedType==="photo")photo.classList.add("selected");
  photo.style.left=`${state.photoX}%`;photo.style.top=`${state.photoY}%`;photo.style.width=`${state.photoWidth}%`;photo.style.aspectRatio="1 / 1";
  const photoImage=document.createElement("img");photoImage.src=state.photoDataUrl;photoImage.alt="Uploaded photo";photo.appendChild(photoImage);
  const handle=document.createElement("div");handle.className="resize-handle";photo.appendChild(handle);
  container.appendChild(photo);enablePhotoDragging(photo,container);enablePhotoResize(handle,photo,container);
 }
 previewArea.appendChild(container);
}

function enableTextDragging(element,container,field){
 let dragging=false,offsetX=0,offsetY=0;
 element.addEventListener("pointerdown",event=>{
  event.preventDefault();state.selectedId=field.id;state.selectedType="text";dragging=true;
  const rect=element.getBoundingClientRect();offsetX=event.clientX-rect.left;offsetY=event.clientY-rect.top;element.classList.add("dragging");element.setPointerCapture(event.pointerId);
 });
 element.addEventListener("pointermove",event=>{
  if(!dragging)return;
  const rect=container.getBoundingClientRect();
  let x=((event.clientX-rect.left-offsetX)/rect.width)*100;let y=((event.clientY-rect.top-offsetY)/rect.height)*100;
  x=Math.max(0,Math.min(100,x));y=Math.max(0,Math.min(100,y));field.x=x;field.y=y;element.style.left=`${x}%`;element.style.top=`${y}%`;
 });
 element.addEventListener("pointerup",()=>{dragging=false;element.classList.remove("dragging");renderPreview()});
}

function enablePhotoDragging(element,container){
 let dragging=false,offsetX=0,offsetY=0;
 element.addEventListener("pointerdown",event=>{
  if(event.target.classList.contains("resize-handle"))return;
  event.preventDefault();state.selectedType="photo";state.selectedId="photo";dragging=true;
  const rect=element.getBoundingClientRect();offsetX=event.clientX-rect.left;offsetY=event.clientY-rect.top;element.classList.add("dragging");element.setPointerCapture(event.pointerId);
 });
 element.addEventListener("pointermove",event=>{
  if(!dragging)return;
  const rect=container.getBoundingClientRect();
  let x=((event.clientX-rect.left-offsetX)/rect.width)*100;let y=((event.clientY-rect.top-offsetY)/rect.height)*100;
  x=Math.max(0,Math.min(100,x));y=Math.max(0,Math.min(100,y));state.photoX=x;state.photoY=y;element.style.left=`${x}%`;element.style.top=`${y}%`;
 });
 element.addEventListener("pointerup",()=>{dragging=false;element.classList.remove("dragging");renderPreview()});
}

function enablePhotoResize(handle,photo,container){
 let resizing=false;
 handle.addEventListener("pointerdown",event=>{event.preventDefault();event.stopPropagation();resizing=true;handle.setPointerCapture(event.pointerId)});
 handle.addEventListener("pointermove",event=>{
  if(!resizing)return;
  const rect=container.getBoundingClientRect();const photoRect=photo.getBoundingClientRect();
  let width=((event.clientX-photoRect.left)/rect.width)*100;width=Math.max(5,Math.min(80,width));state.photoWidth=width;photo.style.width=`${width}%`;
 });
 handle.addEventListener("pointerup",()=>{resizing=false;renderPreview()});
}

csvButton.addEventListener("click",()=>csvInput.click());
csvInput.addEventListener("change",async event=>{
 const file=event.target.files?.[0];if(!file)return;
 const parsed=parseCSV(await file.text());state.csvHeaders=parsed.headers;state.csvRows=parsed.rows;
 if(state.csvRows.length===0){showStatus(csvStatus,"No records found in CSV.","error");return}
 showStatus(csvStatus,`<strong>CSV loaded</strong><br>${state.csvRows.length} record(s)<br>Columns: ${state.csvHeaders.join(", ")}`,"success");
 downloadZipButton.style.display="block";downloadZipButton.disabled=false;
});

function parseCSV(text){
 const rows=[];let current="",row=[],insideQuotes=false;
 for(let i=0;i<text.length;i++){
  const char=text[i],next=text[i+1];
  if(char==='"'&&insideQuotes&&next==='"'){current+='"';i++;continue}
  if(char==='"'){insideQuotes=!insideQuotes;continue}
  if(char===","&&!insideQuotes){row.push(current);current="";continue}
  if((char==="\n"||char==="\r")&&!insideQuotes){
   if(char==="\r"&&next==="\n")i++;row.push(current);
   if(row.some(v=>v.trim()!==""))rows.push(row);row=[];current="";continue;
  }
  current+=char;
 }
 if(current!==""||row.length>0){row.push(current);if(row.some(v=>v.trim()!==""))rows.push(row)}
 if(rows.length===0)return{headers:[],rows:[]};
 const headers=rows[0].map(v=>v.trim());
 const dataRows=rows.slice(1).map(values=>{const obj={};headers.forEach((h,i)=>obj[h]=(values[i]??"").trim());return obj});
 return{headers,rows:dataRows};
}

function renderCanvas(row=null){
 return new Promise(resolve=>{
  const image=state.templateImage;const canvas=document.createElement("canvas");canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;const ctx=canvas.getContext("2d");ctx.drawImage(image,0,0);
  state.fields.forEach(field=>{
   let value=field.value;if(row&&Object.prototype.hasOwnProperty.call(row,field.heading))value=row[field.heading];if(value===null||value===undefined)value="";value=String(value);if(!value)return;
   const x=(field.x/100)*canvas.width;const y=(field.y/100)*canvas.height;
   ctx.font=`${field.fontWeight} ${field.fontSize}px ${field.fontFamily}`;ctx.fillStyle=field.color;ctx.textBaseline="top";ctx.fillText(value,x,y);
  });
  if(state.photoImage){
   const x=((state.photoX??65)/100)*canvas.width;const y=((state.photoY??30)/100)*canvas.height;const width=((state.photoWidth??22)/100)*canvas.width;ctx.drawImage(state.photoImage,x,y,width,width);
  }
  resolve(canvas);
 });
}

async function encodeCanvas(canvas,format,quality){
 const mime=format==="jpeg"?"image/jpeg":format==="webp"?"image/webp":"image/png";
 return new Promise(resolve=>canvas.toBlob(blob=>resolve(blob),mime,quality));
}

async function generateSizedImage(canvas){
 const format=formatInput.value,mode=sizeMode.value,target=bytesFromSize();
 if(mode==="none")return await encodeCanvas(canvas,format,.92);
 if(format==="png")return await encodeCanvas(canvas,format,1);
 if(!target)return await encodeCanvas(canvas,format,.92);
 let low=.05,high=.98,best=null;
 for(let i=0;i<12;i++){
  const quality=(low+high)/2;const blob=await encodeCanvas(canvas,format,quality);
  if(mode==="maximum"){
   if(blob.size<=target){best=blob;low=quality}else high=quality;
  }else{
   if(blob.size<target){best=blob;low=quality}else high=quality;
  }
 }
 return best||await encodeCanvas(canvas,format,.05);
}

function downloadBlob(blob,filename){
 const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download=filename;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);
}

downloadButton.addEventListener("click",async()=>{
 if(!state.templateImage)return;
 downloadButton.disabled=true;downloadButton.textContent="Generating...";generationStatus.style.display="none";
 try{
  const canvas=await renderCanvas();const blob=await generateSizedImage(canvas);const format=formatInput.value;const extension=format==="jpeg"?"jpg":format;
  downloadBlob(blob,`generated-image.${extension}`);
  showStatus(generationStatus,`<strong>Generated successfully</strong><br>File size: ${formatBytes(blob.size)}<br>Format: ${format.toUpperCase()}<br>Resolution: ${canvas.width} × ${canvas.height}`,"success");
 }catch(error){console.error(error);showStatus(generationStatus,"Unable to generate the image.","error")}
 downloadButton.disabled=false;downloadButton.textContent="Download Image";
});

downloadZipButton.addEventListener("click",async()=>{
 if(!state.templateImage||state.csvRows.length===0)return;
 downloadZipButton.disabled=true;downloadZipButton.textContent="Generating...";
 try{
  const zip=new JSZip();
  for(let i=0;i<state.csvRows.length;i++){
   const canvas=await renderCanvas(state.csvRows[i]);const blob=await generateSizedImage(canvas);const format=formatInput.value;const extension=format==="jpeg"?"jpg":format;
   zip.file(`generated_${String(i+1).padStart(3,"0")}.${extension}`,blob);
  }
  const zipBlob=await zip.generateAsync({type:"blob"});downloadBlob(zipBlob,"generated-images.zip");
  showStatus(generationStatus,`<strong>Bulk generation complete</strong><br>Generated ${state.csvRows.length} image(s).`,"success");
 }catch(error){console.error(error);showStatus(generationStatus,"Bulk generation failed.","error")}
 downloadZipButton.disabled=false;downloadZipButton.textContent="Generate & Download ZIP";
});

function formatBytes(bytes){
 if(bytes<1024)return bytes+" B";
 if(bytes<1024*1024)return(bytes/1024).toFixed(2)+" KB";
 return(bytes/1024/1024).toFixed(2)+" MB";
}

addField("Name","");
</script>
</body>
</html>
"""

components.html(HTML, height=850, scrolling=True)
