import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {NavigationComponent} from './navigation/navigation.component';
import {LayoutModule} from '@angular/cdk/layout';
import {
  MatToolbarModule,
  MatButtonModule,
  MatSidenavModule,
  MatListModule,
  MatTableModule,
  MatDialogModule,
  MAT_DIALOG_DATA,
} from '@angular/material';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatIconModule, MatIconRegistry} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {PackagesComponent} from './packages/packages.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {BilingComponent} from './biling/biling.component';
import {SubscriptionsComponent} from './subscriptions/subscriptions.component';
import {ConfigComponent} from './config/config.component';
import {LocationStrategy, PathLocationStrategy} from '@angular/common';
import {ComponentsComponent} from './components/components.component';
import {PaymentsComponent} from './payments/payments.component';
import {PackageDetailsComponent} from './package-details/package-details.component';
import {PaginationComponent} from './pagination/pagination.component';
import {CompanySettingsComponent} from './company-settings/company-settings.component';
import {DialogComponent} from './dialog/dialog.component';
import {MatDialogRef} from '@angular/material/dialog';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {ComponentDetailsComponent} from './component-details/component-details.component';
import {PackageCreateComponent} from './package-create/package-create.component';
import {PackageAttachDialogComponent} from './package-attach-dialog/package-attach-dialog.component';
import {MatSelectModule} from '@angular/material/select';
import {InvoicesComponent} from './invoices/invoices.component';
import {LoginComponent} from './login/login.component';
import {LoginGuard} from './login/login.guard';
import {HttpConfigInterceptor} from './interceptor/httpconfig.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    PackagesComponent,
    DashboardComponent,
    BilingComponent,
    SubscriptionsComponent,
    ConfigComponent,
    ComponentsComponent,
    PaymentsComponent,
    PackageDetailsComponent,
    PaginationComponent,
    CompanySettingsComponent,
    DialogComponent,
    ComponentDetailsComponent,
    InvoicesComponent,
    PackageCreateComponent,
    PackageAttachDialogComponent,
    LoginComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    FormsModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatTableModule,
    MatPaginatorModule,
    MatInputModule,
    MatDialogModule,
    MatSnackBarModule,
    MatSelectModule,
  ],
  providers: [
    {provide: LocationStrategy, useClass: PathLocationStrategy},
    {provide: MatDialogRef, useValue: {}},
    {provide: MAT_DIALOG_DATA, useValue: []},
    {provide: HTTP_INTERCEPTORS, useClass: HttpConfigInterceptor, multi: true},
    LoginGuard,
  ],
  bootstrap: [AppComponent],
  entryComponents: [DialogComponent, DialogComponent, PackageAttachDialogComponent],
})
export class AppModule {
  constructor(private matIconRegistry: MatIconRegistry) {
    matIconRegistry.registerFontClassAlias('mat-icon');
  }
}
