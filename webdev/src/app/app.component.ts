import { Component, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  currentImage = "assets/image/default.png";
  results: Array<any>;
  @ViewChild('fileInput') inputEl: ElementRef;

  constructor(private service: ApiService) {
    
  }

  classificar() {
    let inputEl: HTMLInputElement = this.inputEl.nativeElement;
    let fileCount: number = inputEl.files.length;
    let formData = new FormData();
    if (fileCount > 0) { // a file was selected
      for (let i = 0; i < fileCount; i++) {
        formData.append('file', inputEl.files.item(i));
      }
      this.service.classify(formData).subscribe(response => {
        this.results = response.json();
      }, error => {
        this.results = null;
      });
    }
  }

  onSelectFile(event) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]); // read file as data url

      reader.onload = (event) => { // called once readAsDataURL is completed 
        let e:any = event.target;
        this.currentImage = e.result;
        this.classificar();
      }
    }
  }



}
