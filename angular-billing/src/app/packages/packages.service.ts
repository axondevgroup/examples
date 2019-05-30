import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Packages} from './packages.interface';

@Injectable({
  providedIn: 'root',
})
export class PackagesService {
  constructor(private http: HttpClient) {}

  public getAllPackages(): Observable<Packages[]> {
    return this.http.get<Packages[]>('/packages');
  }
}
