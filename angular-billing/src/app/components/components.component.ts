import {Component, OnInit, ViewChild} from '@angular/core';
import {Observable} from 'rxjs';
import {MatPaginator} from '@angular/material';
import {Components} from './components.interface';
import {AppService} from '../app.service';
import {Pagination} from '../pagination/pagination.interface';
import {defaultPaginationLimitOptions} from '../variables';

@Component({
  selector: 'app-components',
  templateUrl: './components.component.html',
  styleUrls: ['./components.component.scss'],
})
export class ComponentsComponent implements OnInit {
  public displayedColumns: string[] = ['codeColumn', 'nameColumn', 'idColumn', 'typeColumn', 'linksColumn'];
  public dataSource: Components[];
  public pageLength: number;
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;

  @ViewChild(MatPaginator) public paginator: MatPaginator;

  constructor(private service: AppService) {}

  public ngOnInit() {
    this.getComponents();
  }

  private getComponents(skip: number = 0, limit: number = 10) {
    this.service.getAllComponents(skip, limit).subscribe(
      response => {
        this.pageLength = Number(response.headers.get('count'));
        this.dataSource = response.body;
      },
      error => {
        return Observable.throw(error);
      },
    );
  }

  public onNotify(pagination: Pagination): void {
    this.getComponents(pagination.skip, pagination.limit);
  }
}
