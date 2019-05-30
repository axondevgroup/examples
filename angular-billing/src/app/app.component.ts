import {Component, OnInit} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  public isAuth: string;

  constructor(private readonly router: Router) {
    router.events.subscribe(route => {
      if (route instanceof NavigationEnd) {
        if (route.toString().match('dashboard|login')) {
          this.isAuth = window.localStorage.getItem('isAuth');
        }
      }
    });
  }

  public ngOnInit() {
    this.isAuth = window.localStorage.getItem('isAuth');
  }
}
