import {Component, OnInit} from '@angular/core';
import {AppService} from '../app.service';
import {Observable} from 'rxjs';
import {ComponentDetails} from './component-details.interface';
import {ActivatedRoute} from '@angular/router';
import {Pagination} from '../pagination/pagination.interface';
import {defaultPaginationLimitOptions} from '../variables';

@Component({
  selector: 'app-component-details',
  templateUrl: './component-details.component.html',
  styleUrls: ['./component-details.component.scss'],
})
export class ComponentDetailsComponent implements OnInit {
  public componentDetails: ComponentDetails;
  public displayedCompanyDetailsColumns: string[] = ['packageCode', 'quota', 'rate'];
  public pageSize = 10;
  public pageSizeOptions: number[] = defaultPaginationLimitOptions;
  public length: number = 10;

  constructor(private service: AppService, private route: ActivatedRoute) {}

  public ngOnInit() {
    this.getComponents();
  }

  public getComponents(skip = 0, limit = 10) {
    this.route.params.subscribe(params => {
      this.service.getComponentDetails(params.id, skip, limit).subscribe(
        response => {
          this.componentDetails = response;
        },
        error => Observable.throw(error),
      );
    });
  }

  public onNotify(pagination: Pagination): void {
    this.getComponents(pagination.skip, pagination.limit);
  }
}
