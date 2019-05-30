import {Component, OnInit, ViewChild, ErrorHandler} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Observable} from 'rxjs';
import {MatPaginator, MatDialog, MatSnackBar} from '@angular/material';
import {DialogComponent} from '../dialog/dialog.component';
import {AppService} from '../app.service';
import {Pagination} from '../pagination/pagination.interface';
import {defaultPaginationLimitOptions, TableType} from '../variables';

@Component({
  selector: 'app-package-details',
  templateUrl: './package-details.component.html',
  styleUrls: ['./package-details.component.scss'],
})
export class PackageDetailsComponent implements OnInit {
  public componentLength: number;
  public componentNext: boolean;
  public serviceLength: number;
  public serviceNext: boolean;
  public packageDetails: any;
  public componentsTable: any;
  public displayedComponentsColumns: string[] = ['componentCodeColumn', 'componentNameColumn', 'componentRateColumn'];
  public displayedServicesColumns: string[] = ['serviceCodeColumn', 'serviceNameColumn', 'serviceRateColumn'];
  public serviceTable: any;
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;

  @ViewChild(MatPaginator) public componentsPaginator: MatPaginator;
  @ViewChild(MatPaginator) public servicePaginator: MatPaginator;

  constructor(
    public service: AppService,
    private route: ActivatedRoute,
    public dialog: MatDialog,
    private router: Router,
    private snackBar: MatSnackBar,
    private error: ErrorHandler,
  ) {}

  public servicesPagination: Pagination = {
    skip: 0,
    limit: 10,
  };

  public componentsPagination: Pagination = {
    skip: 0,
    limit: 10,
  };

  public ngOnInit() {
    this.getPackages();
  }

  private getPackages(
    serviceSkip: number = 0,
    serviceLimit: number = 10,
    componentSkip: number = 0,
    componentLimit: number = 10,
  ) {
    this.route.params.subscribe(params => {
      this.service.getPackageByCode(params.id, serviceSkip, serviceLimit, componentSkip, componentLimit).subscribe(
        response => {
          this.componentLength = Number(response.headers.get('component_count'));
          this.componentNext = response.headers.get('component_next') === 'true';
          this.serviceLength = Number(response.headers.get('service_count'));
          this.serviceNext = response.headers.get('service_next') === 'true';

          this.packageDetails = response.body;
          this.componentsTable = this.packageDetails.components;
          this.serviceTable = this.packageDetails.service;
        },
        error => {
          this.router.navigateByUrl('/app/packages');
          return this.error.handleError(error);
        },
      );
    });
  }

  public onNotify(pagination: Pagination, packageDetailsTableType: TableType): void {
    if (packageDetailsTableType === 'components') {
      this.componentsPagination = {
        skip: pagination.skip,
        limit: pagination.limit,
      };

      this.getPackages(this.servicesPagination.skip, this.servicesPagination.limit, pagination.skip, pagination.limit);
    } else {
      this.servicesPagination = {
        skip: pagination.skip,
        limit: pagination.limit,
      };

      this.getPackages(
        pagination.skip,
        pagination.limit,
        this.componentsPagination.skip,
        this.componentsPagination.limit,
      );
    }
  }

  public removePackage(packageCode: number, packageName: string): void {
    const dialogRef = this.dialog.open(DialogComponent, {
      panelClass: 'delete-package-dialog',
      data: {
        id: packageCode,
        title: 'Delete Package',
        description: `Are you sure you want to delete \`${packageName}\` package?`,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!!result) {
        this.service.deletePackageByCode(result.id).subscribe(
          () => {
            this.router.navigateByUrl('/app/packages');
          },
          ({error}) => {
            this.snackBar.open(error.message, '', {
              duration: 2000,
              verticalPosition: 'top',
              horizontalPosition: 'right',
              panelClass: 'error-message',
            });
          },
        );
      }
    });
  }
}
