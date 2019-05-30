import {Component} from '@angular/core';
import {AppService} from '../app.service';
import {FormControl, Validators} from '@angular/forms';
import {StateMatcher} from '../state-matcher';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  public email = new FormControl('', [Validators.required, Validators.email]);
  public password = new FormControl('', [Validators.required, Validators.pattern(/[a-z{2}]/)]);

  public matcher = new StateMatcher();

  constructor(private readonly appService: AppService, private route: Router) {}

  public handleSubmit($event) {
    $event.preventDefault();

    this.appService.postAuthCredentials(this.email.value, this.password.value).subscribe(
      response => {
        window.localStorage.setItem('permission', JSON.stringify([response.body.permission]));
        window.localStorage.setItem('isAuth', JSON.stringify(true));

        this.route.navigateByUrl('/app/dashboard');
      },
      error => {
        this.email.setErrors(error.message);
        this.password.setErrors(error.message);
      },
    );
  }
}
