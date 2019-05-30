import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Payments} from './payments.interface';

@Injectable({
  providedIn: 'root',
})
export class PaymentsService {
  constructor(private http: HttpClient) {}

  public getPayments(skip: number = 0, limit: number = 10): Observable<HttpResponse<Payments[]>> {
    return this.http.get<Payments[]>(`/payments?skip=${skip}&limit=${limit}`, {
      observe: 'response',
    });
  }
}
