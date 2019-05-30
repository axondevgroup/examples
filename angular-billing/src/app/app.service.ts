import {Injectable} from '@angular/core';
import {HttpClient, HttpParams, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {CompanySettings} from './company-settings/company-settings.interface';
import {PackageDetails} from './package-details/package-details.interface';
import {ComponentDetails} from './component-details/component-details.interface';
import {Components} from './components/components.interface';
import {Invoice} from './invoices/invoice.interface';
import {Login} from './login/login.interface';
import {environment} from '../environments/environment.prod';
import {AttachPackage, AttachedPackage, ComponentList, ServicesList} from './package-create/package-create.interface';

@Injectable({
  providedIn: 'root',
})
export class AppService {
  constructor(private http: HttpClient) {}

  public getCompanyDetails(): Observable<CompanySettings> {
    return this.http.get<CompanySettings>(`/company/details`, {withCredentials: true});
  }

  public putCompanyDetails(companyUpdate: CompanySettings): Observable<CompanySettings> {
    return this.http.put<CompanySettings>(
      '/company/details',
      {
        due_date: companyUpdate.due_date,
        due_date_type: companyUpdate.due_date_type,
        name: companyUpdate.name,
        over_due: companyUpdate.over_due,
        webhook_url: companyUpdate.webhook_url,
      },
      {withCredentials: true},
    );
  }

  public getPackageByCode(
    code: string,
    serviceSkip: number = 0,
    serviceLimit: number = 10,
    componentSkip: number = 0,
    componentLimit: number = 10,
  ): Observable<HttpResponse<PackageDetails[]>> {
    return this.http.get<PackageDetails[]>(
      `/packages/${code}?serviceSkip=${serviceSkip}&serviceLimit=${serviceLimit}&componentSkip=${componentSkip}&componentLimit=${componentLimit}`,
      {
        observe: 'response',
        withCredentials: true,
      },
    );
  }

  public deletePackageByCode(packageCode: string): Observable<{}> {
    const params = new HttpParams().set('package_code', packageCode);

    return this.http.delete('/packages', {params, withCredentials: true});
  }

  public getComponentDetails(code: string, skip: number, limit: number): Observable<ComponentDetails> {
    return this.http.get<ComponentDetails>(`/components/${code}?skip=${skip}&limit=${limit}`, {withCredentials: true});
  }

  public getAllComponents(skip: number = 0, limit: number = 10): Observable<HttpResponse<Components[]>> {
    return this.http.get<Components[]>(`/components?skip=${skip}&limit=${limit}`, {
      observe: 'response',
      withCredentials: true,
    });
  }

  public getCompaniesServices(skip: number, limit: number): Observable<HttpResponse<ServicesList[]>> {
    return this.http.get<ServicesList[]>(`/packages/services?skip=${skip}&limit=${limit}`, {
      observe: 'response',
    });
  }

  public getCompaniesComponents(skip: number, limit: number): Observable<HttpResponse<ComponentList[]>> {
    return this.http.get<ComponentList[]>(`/packages/components?skip=${skip}&limit=${limit}`, {
      observe: 'response',
    });
  }

  public putUpdatePackage(data: AttachPackage): Observable<AttachedPackage> {
    return this.http.put<AttachedPackage>(`/packages/update-package`, {data});
  }

  public deletePackageByPackageCode(packageCode): Observable<HttpResponse<any>> {
    const params = new HttpParams().set('package_code', packageCode);

    return this.http.delete<any>('/packages/delete-package', {params});
  }

  public getCompanyInvoices(skip: number = 0, limit: number = 10): Observable<HttpResponse<Invoice[]>> {
    return this.http.get<Invoice[]>(`/invoices?skip=${skip}&limit=${limit}`, {
      observe: 'response',
    });
  }

  public postAuthCredentials(email: string, password: string): Observable<HttpResponse<Login>> {
    return this.http.post<Login>(
      `/auth/login`,
      {
        email,
        password,
        clientId: environment.clientId,
      },
      {
        observe: 'response',
        withCredentials: true,
      },
    );
  }
}
