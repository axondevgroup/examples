import {Injectable} from '@angular/core';
import {CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router} from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class LoginGuard implements CanActivate {
  constructor(private readonly route: Router) {}

  public canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (window.localStorage.getItem('isAuth')) {
      return true;
    }

    this.route.navigate(['/login'], {
      queryParams: {
        returnUrl: state.url,
      },
    });
    return false;
  }
}
