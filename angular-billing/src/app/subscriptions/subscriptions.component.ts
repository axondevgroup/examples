import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {SubscriptionsService} from './subscriptions.service';
import {Observable} from 'rxjs';
import {MatPaginator, PageEvent} from '@angular/material';
import {Subscriptions} from './subscriptions.interface';
import {tap} from 'rxjs/operators';
import {defaultPaginationLimitOptions} from '../variables';

@Component({
  selector: 'app-subscriptions',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.scss'],
})
export class SubscriptionsComponent implements AfterViewInit, OnInit {
  public displayedColumns: string[] = [
    'subscriptionIdColumn',
    'customerColumn',
    'createdAtColumn',
    'removedAtColumn',
    'servicesColumn',
    'componentsColumn',
    'linksColumn',
  ];
  public dataSource: Subscriptions[];
  public length: number;
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;
  public pageEvent: PageEvent;

  @ViewChild(MatPaginator) public paginator: MatPaginator;

  constructor(private service: SubscriptionsService) {}

  public ngOnInit() {
    this.getSubscriptions();
  }

  private getSubscriptions(skip: number = 0, limit: number = 10) {
    this.service.getSubscriptions(skip, limit).subscribe(
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
    this.paginator.page.pipe(tap(() => this.getSubscriptions(this.paginator.pageIndex * 10))).subscribe();
  }
}
