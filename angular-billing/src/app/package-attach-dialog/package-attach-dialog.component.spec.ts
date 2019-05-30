import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PackageAttachDialogComponent } from './package-attach-dialog.component';

describe('PackageAttachDialogComponent', () => {
  let component: PackageAttachDialogComponent;
  let fixture: ComponentFixture<PackageAttachDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PackageAttachDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PackageAttachDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
