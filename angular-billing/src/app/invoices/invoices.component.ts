import {Component, OnInit} from '@angular/core';
import {Invoice} from './invoice.interface';
import {AppService} from '../app.service';
import {throwError} from 'rxjs';
import {defaultPaginationLimitOptions} from '../variables';
import {Pagination} from '../pagination/pagination.interface';
import {Router} from '@angular/router';
import {PackagesService} from '../packages/packages.service';

@Component({
  selector: 'app-invoices',
  templateUrl: './invoices.component.html',
  styleUrls: ['./invoices.component.scss'],
})
export class InvoicesComponent implements OnInit {
  public displayedColumns: string[] = [
    'invoiceId',
    'customer',
    'period',
    'dueDate',
    'outstanding',
    'total',
    'status',
    'links',
  ];
  public dataSource: Invoice[];
  public length: number;
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;

  constructor(private service: AppService, private route: Router) {}

  public ngOnInit() {
    this.getInvoices();
  }

  public getInvoices(skip: number = 0, limit: number = 10) {
    this.service.getCompanyInvoices(skip, limit).subscribe(
      response => {
        this.length = Number(response.headers.get('count'));
        this.dataSource = response.body;
      },
      error => {
        return throwError(error);
      },
    );
  }

  public onNotify(pagination: Pagination): void {
    this.getInvoices(pagination.skip, pagination.limit);
  }

  public getInvoicesDetails(row) {
    this.route.navigateByUrl(`app/invoices/details`);
  }
}
