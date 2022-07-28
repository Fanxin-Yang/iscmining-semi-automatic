import{a as h}from"./index.becf6c0c.js";import{_,o as i,c as o,a as s,t as c,w as p,v as f,F as m,r as b,b as v}from"./index.8bd797c2.js";const F={data(){return{info:void 0,status:null,selectedFile:void 0,dataSet:void 0,selectedFiles:FileList,availableDataSets:void 0,next:!1,projections:{}}},methods:{get_dataSets(){const l="http://localhost:5000/upload";h.get(l).then(t=>{this.availableDataSets=t.data}).catch(t=>{console.error(t),this.status=t.response.status,this.info=t.response.data})},select_files(){this.selectedFiles=this.$refs.file.files},upload_file(l){const t="http://localhost:5000/upload";let d=new FormData;d.append("file",l);const r={"Content-Type":"multipart/form-data"};h.post(t,d,{headers:r}).then(e=>{console.log(e),this.get_dataSets(),this.status=e.status,this.info=e.statusText,this.selectedFile=this.selectedFiles[0].name}).catch(e=>{console.error(e),this.status=e.response.status,this.info=e.response.data})},submit_file(){this.status=-1,this.selectedFiles.length==0&&this.upload_file(this.$refs.file.files[0]);for(let l=0;l<this.selectedFiles.length;l++)this.upload_file(this.selectedFiles[l])},start_preprocess(){let l=this.selectedFile.substring(0,this.selectedFile.lastIndexOf("."));this.$router.replace(l)}},created(){this.get_dataSets()}},g={class:"row g-3"},y=s("h3",{class:"display-4"},"Dataset",-1),k=s("h6",null,"Please select an existing data set or upload a new one.",-1),S={class:"col-md-6"},x={class:"col-md-2"},D={key:0,class:"text-center"},w=s("div",{class:"spinner-border m-5",role:"status"},[s("span",{class:"visually-hidden"},"Loading...")],-1),C=[w],P={key:1,class:"alert alert-danger",role:"alert"},V={key:2,class:"alert alert-warning",role:"alert"},B={key:3,class:"alert alert-success",role:"alert"},L={key:4,class:"alert alert-light",role:"alert"},U={key:5,class:"alert alert-light",role:"alert"},N={key:6,class:"row g-3"},T={class:"col-md-6"},j=s("option",{selected:"",disabled:"",value:""},"Select a data set",-1),E={class:"col-md-4"},I=["disabled"];function M(l,t,d,r,e,n){return i(),o("form",g,[y,k,s("div",S,[s("input",{class:"form-control",type:"file",multiple:"",id:"formFile",onChange:t[0]||(t[0]=(...a)=>n.select_files&&n.select_files(...a)),ref:"file"},null,544)]),s("div",x,[s("button",{type:"button",class:"btn btn-outline-primary",onClick:t[1]||(t[1]=(...a)=>n.submit_file&&n.submit_file(...a))}," Upload ")]),e.status==-1?(i(),o("div",D,C)):e.status==400?(i(),o("div",P,c(e.info),1)):e.status==406?(i(),o("div",V,c(e.info),1)):e.status==200||e.status==0?(i(),o("div",B,c(e.info),1)):this.selectedFiles?(i(),o("div",U," You have choose "+c(this.selectedFiles.length)+' files. Please click the "Upload" button to complete. ',1)):(i(),o("div",L," Please choose a .xes file and click the upload button. ")),e.status!=404?(i(),o("div",N,[s("div",T,[p(s("select",{"onUpdate:modelValue":t[2]||(t[2]=a=>e.selectedFile=a),class:"form-select"},[j,(i(!0),o(m,null,b(e.availableDataSets,(a,u)=>(i(),o("option",{key:u},c(a),1))),128))],512),[[f,e.selectedFile]])]),s("div",E,[s("button",{type:"button",class:"btn btn-primary",onClick:t[3]||(t[3]=(...a)=>n.start_preprocess&&n.start_preprocess(...a)),disabled:!e.selectedFile}," Start Pre-process ",8,I)]),s("h4",null,"Selected data set: "+c(e.selectedFile),1)])):v("",!0)])}var q=_(F,[["render",M]]);export{q as default};
