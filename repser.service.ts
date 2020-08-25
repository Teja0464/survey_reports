import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import * as _ from 'lodash';

@Injectable({
  providedIn: 'root'
})
export class RepserService {


  baseUrl = 'http://127.0.0.1:5000';

  constructor(private http:HttpClient) { }

  getAllIds(){
    return this.http.get<any>(`${this.baseUrl}/getAllIds`);
  }
  getAllhds(){
    return this.http.get<any>(`${this.baseUrl}/getAllhds`);
  }
  getresct(){
    return this.http.get<any>(`${this.baseUrl}/getresct`);
  }
  getorct(){
    return this.http.get<any>(`${this.baseUrl}/getorct`);
  }
  getevy(){
    return this.http.get<any>(`${this.baseUrl}/getevy`);
  }
  getsubs(para){
    return this.http.post<any>(`${this.baseUrl}/getsubs`,para);
  }
  getsubsbyhd(para){
    return this.http.post<any>(`${this.baseUrl}/getsubsbyhd`,para);
  }
  getchartsid(para){
    return this.http.post<any>(`${this.baseUrl}/getchartsid`,para);
  }
  getchartshd(para){
    return this.http.post<any>(`${this.baseUrl}/getchartshd`,para);
  }
  getsubchart(para){
    return this.http.post<any>(`${this.baseUrl}/getsubchart`,para);
  }




  getDropText(id, object){
    const selObj = _.filter(object, function (o) {
      return (_.includes(id,o.id));
    });
    return selObj;
  }
}
