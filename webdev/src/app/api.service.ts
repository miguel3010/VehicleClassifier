import { Injectable } from '@angular/core';

import { Http, Response, RequestOptions } from '@angular/http'; 
import { HttpParams } from '@angular/common/http';
import { stringify } from '@angular/core/src/util';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseURL = 'http://127.0.0.1:5000';

  constructor(private http: Http) { }
  classify(image) {    

    return this.http.post(this.baseURL + '/api/classify', image);

  }
}
