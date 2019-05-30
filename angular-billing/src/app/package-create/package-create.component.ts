import {Component, OnInit} from '@angular/core';
import {defaultPaginationLimitOptions, TableType} from '../variables';
import {Pagination} from '../pagination/pagination.interface';
import {FormControl, Validators} from '@angular/forms';
import {fieldValidation, nameValidation, rateValidation} from '../pattern';
import {ServicesList, ComponentList} from './package-create.interface';
import {MatDialog} from '@angular/material';
import {AppService} from '../app.service';
import {Observable} from 'rxjs';
import {PackageAttachDialogComponent} from '../package-attach-dialog/package-attach-dialog.component';
import {MatTableDataSource} from '@angular/material/table';
import {Router} from '@angular/router';

@Component({
  selector: 'app-package-create',
  templateUrl: './package-create.component.html',
  styleUrls: ['./package-create.component.scss'],
})
export class PackageCreateComponent implements OnInit {
  public displayedServicesColumns: string[] = ['serviceCode', 'name'];
  public displayedComponentsColumns: string[] = ['componentsCode', 'name', 'rate'];
  public serviceTable: ServicesList[];
  public componentsTable: ComponentList[];
  public serviceLength: number = 0;
  public componentsLength: number = 0;
  public pageSize: number = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;
  public attachedServiceTable = new MatTableDataSource<ServicesList[]>();
  public attachedComponentTable = new MatTableDataSource<ComponentList[]>();

  public name = new FormControl('', [Validators.required, Validators.pattern(nameValidation)]);
  public code = new FormControl('', [Validators.required, Validators.pattern(fieldValidation)]);
  public rate = new FormControl('', [Validators.required, Validators.pattern(rateValidation)]);

  constructor(public dialog: MatDialog, private service: AppService, private router: Router) {}

  public servicesPagination: Pagination = {
    skip: 0,
    limit: 10,
  };

  public componentsPagination: Pagination = {
    skip: 0,
    limit: 10,
  };

  protected servicesList: any = [];
  protected componentsList: any = [];

  public ngOnInit() {
    this.getAllServices();
    this.getAllComponents();
  }

  public getAllServices(skip: number = 0, limit: number = 50) {
    this.service.getCompaniesServices(skip, limit).subscribe(
      response => {
        this.serviceTable = response.body;
      },
      error => {
        return Observable.throw(error);
      },
    );
  }

  public getAllComponents(skip: number = 0, limit: number = 50) {
    this.service.getCompaniesComponents(skip, limit).subscribe(
      response => {
        this.componentsTable = response.body;
      },
      error => {
        return Observable.throw(error);
      },
    );
  }

  public attachTo(tableType) {
    if (tableType === 'services') {
      const dialogRef = this.dialog.open(PackageAttachDialogComponent, {
        panelClass: 'delete-package-dialog',
        data: {
          title: 'Services',
          selectList: this.serviceTable,
          type: 'Services',
          formValues: {},
        },
      });

      dialogRef.afterClosed().subscribe(result => {
        if (!!result) {
          this.service
            .putUpdatePackage({
              name: this.name.value,
              code: this.code.value,
              monthly_rate: Number(this.rate.value),
              services: [
                {
                  service_id: result.selectedName,
                },
              ],
              components: [],
            })
            .subscribe(
              response => {
                this.serviceTable = this.serviceTable.filter(service => service.service_code !== response.service_code);
                this.servicesList.push(response);
                this.attachedServiceTable = new MatTableDataSource(this.servicesList);
                this.attachedComponentTable._updateChangeSubscription();
                this.serviceLength = this.servicesList.length;
                this.code.setValue('');
              },
              error => {
                return Observable.throw(error);
              },
            );
        }
      });
    } else {
      const dialogRef = this.dialog.open(PackageAttachDialogComponent, {
        panelClass: 'delete-package-dialog',
        data: {
          title: 'Including Component to the Package:',
          selectList: this.componentsTable,
          type: 'Component',
          formValues: {},
        },
      });

      dialogRef.afterClosed().subscribe(result => {
        if (!!result) {
          this.service
            .putUpdatePackage({
              name: this.name.value,
              code: this.code.value,
              monthly_rate: Number(this.rate.value),
              services: [],
              components: [
                {
                  component_id: result.selectedName,
                  rate: Number(result.rate),
                  rate_type: result.type,
                  quota: Number(result.quota),
                },
              ],
            })
            .subscribe(
              response => {
                this.componentsTable = this.componentsTable.filter(component => {
                  return component.name !== response.components[0].name;
                });
                this.componentsList.push(response);
                this.attachedComponentTable = new MatTableDataSource(this.componentsList);
                this.attachedComponentTable._updateChangeSubscription();
                this.componentsLength = this.componentsList.length;
                this.code.setValue('');
              },
              error => {
                return Observable.throw(error);
              },
            );
        }
      });
    }
  }

  public onNotify(pagination: Pagination, packageDetailsTableType: TableType): void {
    if (packageDetailsTableType === 'components') {
      this.componentsPagination = {
        skip: pagination.skip,
        limit: pagination.limit,
      };

      this.getAllComponents(this.componentsPagination.skip, this.componentsPagination.limit);
    } else {
      this.servicesPagination = {
        skip: pagination.skip,
        limit: pagination.limit,
      };
      this.getAllServices(this.servicesPagination.skip, this.servicesPagination.limit);
    }
  }

  public doneCratePackage() {
    this.router.navigateByUrl('/app/packages');
  }

  public deleteIncludedItem(tableRow, rowType) {
    if (rowType === 'components') {
      this.service.deletePackageByPackageCode(tableRow.package_code).subscribe(
        () => {
          this.componentsList = this.componentsList.filter(component => {
            return component.package_code !== tableRow.package_code;
          });
          this.attachedComponentTable = new MatTableDataSource(this.componentsList);
          this.attachedComponentTable._updateChangeSubscription();
          this.componentsLength = this.componentsList.length;
        },
        error => {
          return Observable.throw(error);
        },
      );
    } else {
      this.service.deletePackageByPackageCode(tableRow.package_code).subscribe(
        () => {
          this.servicesList = this.servicesList.filter(component => {
            return component.package_code !== tableRow.package_code;
          });
          this.attachedServiceTable = new MatTableDataSource(this.servicesList);
          this.attachedServiceTable._updateChangeSubscription();
          this.serviceLength = this.servicesList.length;
        },
        error => {
          return Observable.throw(error);
        },
      );
    }
  }
}
