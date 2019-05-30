import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Subscriptions} from './subscriptions.interface';

@Injectable({
  providedIn: 'root',
})
export class SubscriptionsService {
  constructor(private http: HttpClient) {}

  public getSubscriptions(skip: number = 0, limit: number = 10): Observable<HttpResponse<Subscriptions[]>> {
    return this.http.get<Subscriptions[]>(`/subscription/list?skip=${skip}&limit=${limit}`, {
      observe: 'response',
    });
  }
}
