import{_,b as u,o as i,c as a,a as t,t as c,w as f,v as p,F as m,r as b,d as v}from"./index.1548a765.js";const F={data(){return{info:void 0,status:null,selectedFile:void 0,dataSet:void 0,selectedFiles:FileList,availableDataSets:void 0,next:!1,projections:{}}},methods:{get_dataSets(){u.get("upload").then(e=>{this.availableDataSets=e.data}).catch(e=>{console.error(e),this.status=e.response.status,this.info=e.response.data})},select_files(){this.selectedFiles=this.$refs.file.files},upload_file(e){let l=new FormData;l.append("file",e);const r={"Content-Type":"multipart/form-data"};u.post("upload",l,{headers:r}).then(n=>{console.log(n),this.get_dataSets(),this.status=n.status,this.info=n.statusText,this.selectedFile=this.selectedFiles[0].name}).catch(n=>{console.error(n),this.status=n.response.status,this.info=n.response.data})},submit_file(){this.status=-1,this.selectedFiles.length==0&&this.upload_file(this.$refs.file.files[0]);for(let e=0;e<this.selectedFiles.length;e++)this.upload_file(this.selectedFiles[e])},start_preprocess(){let e=this.selectedFile.substring(0,this.selectedFile.lastIndexOf("."));this.$router.replace(e)}},created(){this.get_dataSets()}},g={class:"row g-3"},y=t("h3",{class:"display-4"},"Dataset",-1),k=t("h6",null,"Please select an existing data set or upload a new one.",-1),S={class:"col-md-6"},x={class:"col-md-2"},D={key:0,class:"text-center"},w=t("div",{class:"spinner-border m-5",role:"status"},[t("span",{class:"visually-hidden"},"Loading...")],-1),C=[w],P={key:1,class:"alert alert-danger",role:"alert"},V={key:2,class:"alert alert-warning",role:"alert"},B={key:3,class:"alert alert-success",role:"alert"},L={key:4,class:"alert alert-light",role:"alert"},U={key:5,class:"alert alert-light",role:"alert"},N={key:6,class:"row g-3"},T={class:"col-md-6"},j=t("option",{selected:"",disabled:"",value:""},"Select a data set",-1),E={class:"col-md-4"},I=["disabled"];function M(e,l,r,n,s,d){return i(),a("form",g,[y,k,t("div",S,[t("input",{class:"form-control",type:"file",multiple:"",id:"formFile",onChange:l[0]||(l[0]=(...o)=>d.select_files&&d.select_files(...o)),ref:"file"},null,544)]),t("div",x,[t("button",{type:"button",class:"btn btn-outline-primary",onClick:l[1]||(l[1]=(...o)=>d.submit_file&&d.submit_file(...o))}," Upload ")]),s.status==-1?(i(),a("div",D,C)):s.status==400?(i(),a("div",P,c(s.info),1)):s.status==406?(i(),a("div",V,c(s.info),1)):s.status==200||s.status==0?(i(),a("div",B,c(s.info),1)):this.selectedFiles?(i(),a("div",U," You have choose "+c(this.selectedFiles.length)+' files. Please click the "Upload" button to complete. ',1)):(i(),a("div",L," Please choose a .xes file and click the upload button. ")),s.status!=404?(i(),a("div",N,[t("div",T,[f(t("select",{"onUpdate:modelValue":l[2]||(l[2]=o=>s.selectedFile=o),class:"form-select"},[j,(i(!0),a(m,null,b(s.availableDataSets,(o,h)=>(i(),a("option",{key:h},c(o),1))),128))],512),[[p,s.selectedFile]])]),t("div",E,[t("button",{type:"button",class:"btn btn-primary",onClick:l[3]||(l[3]=(...o)=>d.start_preprocess&&d.start_preprocess(...o)),disabled:!s.selectedFile}," Start Pre-process ",8,I)]),t("h4",null,"Selected data set: "+c(s.selectedFile),1)])):v("",!0)])}var Y=_(F,[["render",M]]);export{Y as default};
