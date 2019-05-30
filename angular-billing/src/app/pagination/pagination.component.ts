import {AfterViewInit, Component, EventEmitter, Input, Output, ViewChild} from '@angular/core';
import {MatPaginator, PageEvent} from '@angular/material';
import {tap} from 'rxjs/operators';
import {Pagination} from './pagination.interface';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss'],
})
export class PaginationComponent implements AfterViewInit {
  @Input() public length: number;
  @Input() public pageSize: number;
  @Input() public pageSizeOptions: number[];

  @Output() public notify: EventEmitter<Pagination> = new EventEmitter<Pagination>();

  @ViewChild(MatPaginator) public paginator: MatPaginator;

  public pageEvent: PageEvent;

  public ngAfterViewInit() {
    this.paginator.page
      .pipe(
        tap(() => {
          this.notify.emit({
            skip: this.paginator.pageIndex * this.paginator.pageSize,
            limit: this.paginator.pageSize,
          });
        }),
      )
      .subscribe();
  }
}
