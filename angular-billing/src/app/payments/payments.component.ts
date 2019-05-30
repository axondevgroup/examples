import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {PaymentsService} from './payments.service';
import {Observable} from 'rxjs';
import {MatPaginator, PageEvent} from '@angular/material';
import {Payments} from './payments.interface';
import {tap} from 'rxjs/operators';
import {defaultPaginationLimitOptions} from '../variables';

@Component({
  selector: 'app-payments',
  templateUrl: './payments.component.html',
  styleUrls: ['./payments.component.scss'],
})
export class PaymentsComponent implements AfterViewInit, OnInit {
  public displayedColumns: string[] = [
    'externalPaymentIdColumn',
    'customerColumn',
    'paymentDateColumn',
    'amountColumn',
    'typeColumn',
    'invoiceIdColumn',
  ];
  public dataSource: Payments[];
  public length: number;
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;
  public pageEvent: PageEvent;

  @ViewChild(MatPaginator) public paginator: MatPaginator;

  constructor(private service: PaymentsService) {}

  public ngOnInit() {
    this.getPayments();
  }

  private getPayments(skip: number = 0, limit: number = 10) {
    this.service.getPayments(skip, limit).subscribe(
      response => {
        this.length = Number(response.headers.get('count'));
        this.dataSource = response.body;
      },
      error => {
        return Observable.throw(error);
      },
    );
  }

  public ngAfterViewInit() {
    this.paginator.page.pipe(tap(() => this.getPayments(this.paginator.pageIndex * 10))).subscribe();
  }
}
