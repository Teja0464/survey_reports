import { Component, OnInit } from '@angular/core';
import { GoogleChartInterface, Ng2GoogleChartsModule } from 'ng2-google-charts';
import { RepserService} from './../repser.service';


@Component({
  selector: 'app-reps',
  templateUrl: './reps.component.html',
  styleUrls: ['./reps.component.css']
})
export class RepsComponent implements OnInit {
  ids:any[] = [];
  selid = "1";
  rescnt = 0;
  orcnt = 0;
  selectedId: any;
  fone = false;
  stwo = false;
  tthree = false;
  pie1: GoogleChartInterface;
  pie2: GoogleChartInterface;
  pie3: GoogleChartInterface;
  

  iform = document.querySelector("idform");
  constructor(private repservice: RepserService) { }

  ngOnInit(): void {
    this.getids();
    this.gethds();
    this.getrescnt();
    this.getorcnt();
    this.getevy();
  }

  getids(){
    this.repservice.getAllIds().subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
        var tbs = "";
            tbs += "<option>Filter by Section number</option>";
            tbs += "<option>All</option>";
            for (var re in rslts) {
                tbs += '<option>' + rslts[re] + '</option>';
                this.ids.push(rslts[re]);
            }
            document.querySelector(".idform").innerHTML = tbs;

    });
  }
  gethds(){
    this.repservice.getAllhds().subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
        var tbs = "";
            tbs += "<option>Filter by Section head</option>";
            for (var re in rslts) {

                tbs += '<option>' + rslts[re] + '</option>';
            }
            document.querySelector(".headform").innerHTML = tbs;

    });
  }
  getsubs(event: any){
    // var tn = (<HTMLInputElement>document.querySelector("idform")).value;
    // this.selectedId = this.repservice.getDropText(this.selid,this.ids);
    // console.log(this.selectedId);
    this.gethds();
    this.fone = false;
    this.stwo = false;
    this.tthree = false;
    this.selectedId = event.target.value;
    if(this.selectedId=="All"){
      this.getevy();
      return;
    }
    console.log(this.selectedId);
    var para = {"id":this.selectedId};
    this.repservice.getsubs(para).subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
        var tbs = "";
            tbs += "<option>Sub Question</option>";
            for (var re in rslts) {

                tbs += '<option>' + rslts[re] + '</option>';
                console.log(rslts[re]);
            }
            document.querySelector(".subform").innerHTML = tbs;

    });
    this.repservice.getchartsid(para).subscribe(resp=>{
      
      console.log(resp);
      var d1 = resp['sd1'];
      var d2 = resp['sd2'];
      var d3 = resp['sd3'];
      const chartData4:any =[['option', 'count']];
      for(var x in d1){
        console.log(d1[x]["option"],d1[x]["count"]);
        chartData4.push([d1[x]["option"],d1[x]["count"]]);
      }
      console.log("This is pie1 " + chartData4);
      this.pie1= {
        chartType: 'PieChart',
        dataTable: chartData4,
        // firstRowIsData: true,
        options: {'title': 'Present status in Karnataka','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.fone = true;

      //2nd chart
      const chartData2:any =[['option', 'count']];
      for(var x in d2){
        console.log(d2[x]["option"],d2[x]["count"]);
        chartData2.push([d2[x]["option"],d2[x]["count"]]);
      }
      
      console.log(chartData2);
      this.pie2= {
        chartType: 'PieChart',
        dataTable: chartData2,
        // firstRowIsData: true,
        options: {'title': 'Nature of implecations','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.stwo = true;
      //3rd chart
      const chartData3:any =[['option', 'count']];
      for(var x in d3){
        console.log(d3[x]["option"],d3[x]["count"]);
        chartData3.push([d3[x]["option"],d3[x]["count"]]);
      }
      
      console.log(chartData3);
      this.pie3= {
        chartType: 'PieChart',
        dataTable: chartData3,
        // firstRowIsData: true,
        options: {'title': 'Implementation time','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.tthree = true;
    });

  }
  getsubsbyhd(event: any){
    // var tn = (<HTMLInputElement>document.querySelector("idform")).value;
    // this.selectedId = this.repservice.getDropText(this.selid,this.ids);
    // console.log(this.selectedId);
    this.getids();
    this.fone = false;
    this.stwo = false;
    this.tthree = false;
     var selectedhd = event.target.value;
    console.log(this.selectedId);
    var para = {"hd":selectedhd};
    this.repservice.getsubsbyhd(para).subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
        var tbs = "";
            tbs += "<option>Sub Question</option>";
            for (var re in rslts) {

                tbs += '<option>' + rslts[re] + '</option>';
                console.log(rslts[re]);
            }
            document.querySelector(".subform").innerHTML = tbs;

    });
    this.repservice.getchartshd(para).subscribe(resp=>{
      
      console.log(resp);
      var d1 = resp['sd1'];
      var d2 = resp['sd2'];
      var d3 = resp['sd3'];
      const chartData4:any =[['option', 'count']];
      for(var x in d1){
        console.log(d1[x]["option"],d1[x]["count"]);
        chartData4.push([d1[x]["option"],d1[x]["count"]]);
      }
      console.log("This is pie1 " + chartData4);
      this.pie1= {
        chartType: 'PieChart',
        dataTable: chartData4,
        // firstRowIsData: true,
        options: {'title': 'Present status in Karnataka','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.fone = true;

      //2nd chart
      const chartData2:any =[['option', 'count']];
      for(var x in d2){
        console.log(d2[x]["option"],d2[x]["count"]);
        chartData2.push([d2[x]["option"],d2[x]["count"]]);
      }
      
      console.log(chartData2);
      this.pie2= {
        chartType: 'PieChart',
        dataTable: chartData2,
        // firstRowIsData: true,
        options: {'title': 'Nature of implecations','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.stwo = true;
      //3rd chart
      const chartData3:any =[['option', 'count']];
      for(var x in d3){
        console.log(d3[x]["option"],d3[x]["count"]);
        chartData3.push([d3[x]["option"],d3[x]["count"]]);
      }
      
      console.log(chartData3);
      this.pie3= {
        chartType: 'PieChart',
        dataTable: chartData3,
        // firstRowIsData: true,
        options: {'title': 'Implementation time','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.tthree = true;
    });

  }

  getrescnt(){
    this.repservice.getresct().subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
      this.rescnt = rslts;
    });
  }
  getorcnt(){
    this.repservice.getorct().subscribe(resp=>{
      console.log(resp);
      var rslts = resp['message'];
      this.orcnt = rslts;
    });
  }
  getevy(){
    this.repservice.getevy().subscribe(resp=>{
      console.log(resp);
      var d1 = resp['sd1'];
      var d2 = resp['sd2'];
      var d3 = resp['sd3'];
      const chartData:any =[['option', 'count']];
      for(var x in d1){
        console.log(d1[x]["option"],d1[x]["count"]);
        chartData.push([d1[x]["option"],d1[x]["count"]]);
      }
      
      console.log(chartData);
      this.fone = true;
      this.pie1= {
        chartType: 'PieChart',
        dataTable: chartData,
        // firstRowIsData: true,
        options: {'title': 'Present status in Karnataka','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };

      //2nd chart
      const chartData2:any =[['option', 'count']];
      for(var x in d2){
        console.log(d2[x]["option"],d2[x]["count"]);
        chartData2.push([d2[x]["option"],d2[x]["count"]]);
      }
      
      console.log(chartData2);
      this.stwo = true;
      this.pie2= {
        chartType: 'PieChart',
        dataTable: chartData2,
        // firstRowIsData: true,
        options: {'title': 'Nature of implecations','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      //3rd chart
      const chartData3:any =[['option', 'count']];
      for(var x in d3){
        console.log(d3[x]["option"],d3[x]["count"]);
        chartData3.push([d3[x]["option"],d3[x]["count"]]);
      }
      
      console.log(chartData3);
      this.tthree = true;
      this.pie3= {
        chartType: 'PieChart',
        dataTable: chartData3,
        // firstRowIsData: true,
        options: {'title': 'Implementation time','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      

    });
    
  }

  getresults(event : any){
    this.fone = false;
    this.stwo = false;
    this.tthree = false;
    var subq = event.target.value;
    var para = {"sub":subq};
    this.repservice.getsubchart(para).subscribe(resp=>{
      
      console.log(resp);
      var d1 = resp['sd1'];
      var d2 = resp['sd2'];
      var d3 = resp['sd3'];
      const chartData4:any =[['option', 'count']];
      for(var x in d1){
        console.log(d1[x]["option"],d1[x]["count"]);
        chartData4.push([d1[x]["option"],d1[x]["count"]]);
      }
      console.log("This is pie1 " + chartData4);
      this.pie1= {
        chartType: 'PieChart',
        dataTable: chartData4,
        // firstRowIsData: true,
        options: {'title': 'Present status in Karnataka','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.fone = true;

      //2nd chart
      const chartData2:any =[['option', 'count']];
      for(var x in d2){
        console.log(d2[x]["option"],d2[x]["count"]);
        chartData2.push([d2[x]["option"],d2[x]["count"]]);
      }
      
      console.log(chartData2);
      this.pie2= {
        chartType: 'PieChart',
        dataTable: chartData2,
        // firstRowIsData: true,
        options: {'title': 'Nature of Implications','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.stwo = true;
      //3rd chart
      const chartData3:any =[['option', 'count']];
      for(var x in d3){
        console.log(d3[x]["option"],d3[x]["count"]);
        chartData3.push([d3[x]["option"],d3[x]["count"]]);
      }
      
      console.log(chartData3);
      this.pie3= {
        chartType: 'PieChart',
        dataTable: chartData3,
        // firstRowIsData: true,
        options: {'title': 'Implementation time','backgroundColor':'#5fdde5','width':400, 'height':300, 'titleTextStyle':{'fontSize':'15','fontFamily':'Roboto, sans-serif'}},
      };
      this.tthree = true;
    });
    console.log(subq);
  }





}
