import {Injectable} from '@angular/core';
import {HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse} from '@angular/common/http';

import {Observable, throwError} from 'rxjs';
import {map, catchError} from 'rxjs/operators';
import {Router} from '@angular/router';

@Injectable()
export class HttpConfigInterceptor implements HttpInterceptor {
  constructor(private readonly route: Router) {}

  public intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      map((event: HttpEvent<any>) => {
        return event;
      }),
      catchError((error: HttpErrorResponse) => {
        if (error.status === 403) {
          this.route.navigateByUrl('login');
        }
        window.localStorage.removeItem('isAuth');
        window.localStorage.removeItem('permission');
        return throwError(error);
      }),
    );
  }
}
