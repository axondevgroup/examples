import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PackagesComponent} from './packages/packages.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {BilingComponent} from './biling/biling.component';
import {SubscriptionsComponent} from './subscriptions/subscriptions.component';
import {ConfigComponent} from './config/config.component';
import {ComponentsComponent} from './components/components.component';
import {PaymentsComponent} from './payments/payments.component';
import {PackageDetailsComponent} from './package-details/package-details.component';
import {CompanySettingsComponent} from './company-settings/company-settings.component';
import {ComponentDetailsComponent} from './component-details/component-details.component';
import {PackageCreateComponent} from './package-create/package-create.component';
import {InvoicesComponent} from './invoices/invoices.component';
import {LoginComponent} from './login/login.component';
import {LoginGuard} from './login/login.guard';

const routes: Routes = [
  {path: 'login', component: LoginComponent, pathMatch: 'full'},
  {path: 'login', redirectTo: '/app/dashboard', pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/dashboard', component: DashboardComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: '', redirectTo: '/app/dashboard', pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/billing', component: BilingComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/subscriptions', component: SubscriptionsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/packages', component: PackagesComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/packages/create', component: PackageCreateComponent, pathMatch: 'full'},
  {path: 'app/packages/:id', component: PackageDetailsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/components', component: ComponentsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/components/:id', component: ComponentDetailsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/config', component: ConfigComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/payments', component: PaymentsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/settings', component: CompanySettingsComponent, pathMatch: 'full', canActivate: [LoginGuard]},
  {path: 'app/invoices', component: InvoicesComponent, pathMatch: 'full'},

  {path: '**', redirectTo: 'app/dashboard'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
