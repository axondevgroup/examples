import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {AppService} from '../app.service';
import {CompanySettings} from './company-settings.interface';
import {Observable} from 'rxjs';
import {FormControl, Validators} from '@angular/forms';
import {StateMatcher} from '../state-matcher';
import {urlValidator} from '../pattern';

@Component({
  selector: 'app-integration',
  templateUrl: './company-settings.component.html',
  styleUrls: ['./company-settings.component.scss'],
})
export class CompanySettingsComponent implements OnInit {
  public companySettings: CompanySettings;
  public editWebHookUrl: boolean;
  private webHookCacheLink: string;

  public matcher = new StateMatcher();

  @ViewChild('webHookUrl') public webHookUrl: ElementRef;

  constructor(private service: AppService) {}

  public webHookFormControl = new FormControl('', [Validators.required, Validators.pattern(urlValidator)]);

  public ngOnInit() {
    this.editWebHookUrl = true;

    this.service.getCompanyDetails().subscribe(
      response => {
        this.companySettings = response;
      },
      error => {
        return Observable.throw(error);
      },
    );

    this.webHookCacheLink = this.webHookUrl.nativeElement.value;
  }

  public changeUrl(): void {
    this.editWebHookUrl = false;
    this.webHookUrl.nativeElement.focus();
  }

  public handleFocus(): void {
    this.webHookFormControl.setValue(this.webHookUrl.nativeElement.value);
    this.webHookCacheLink = this.webHookUrl.nativeElement.value;
  }

  public handleBlur(): void {
    this.editWebHookUrl = true;

    if (this.webHookCacheLink !== this.webHookUrl.nativeElement.value && !this.webHookFormControl.errors) {
      this.service
        .putCompanyDetails({...this.companySettings, webhook_url: this.webHookUrl.nativeElement.value})
        .subscribe(
          response => {
            this.companySettings = response;
          },
          error => {
            return Observable.throw(error);
          },
        );
    }
  }
}
