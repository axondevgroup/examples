import {Component, OnInit} from '@angular/core';
import {PackagesService} from './packages.service';
import {Observable} from 'rxjs';
import {Packages} from './packages.interface';
import {Router} from '@angular/router';

@Component({
  selector: 'app-packages',
  templateUrl: './packages.component.html',
  styleUrls: ['./packages.component.scss'],
})
export class PackagesComponent implements OnInit {
  public displayedColumns: string[] = ['codeColumn', 'nameColumn', 'idColumn', 'rateColumn', 'linksColumn'];
  public dataSource: Packages[];

  constructor(private packages: PackagesService, private route: Router) {}

  public ngOnInit() {
    this.packages.getAllPackages().subscribe(
      response => {
        this.dataSource = response;
      },
      error => {
        return Observable.throw(error);
      },
    );
  }

  public getSpecificPackage(row) {
    this.route.navigateByUrl(`app/packages/${row.package_code}`);
  }
}
