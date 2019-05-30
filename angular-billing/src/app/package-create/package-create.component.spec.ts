import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PackageCreateComponent } from './package-create.component';

describe('PackageCreateComponent', () => {
  let component: PackageCreateComponent;
  let fixture: ComponentFixture<PackageCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PackageCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PackageCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
