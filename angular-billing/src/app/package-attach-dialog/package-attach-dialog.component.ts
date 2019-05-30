import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {PackageAttachDialog} from './package-attach-dialog.interface';
import {FormControl, Validators} from '@angular/forms';
import {onlyLiterals, onlyNumbers, packageAttachType} from '../pattern';

@Component({
  selector: 'app-package-attach-dialog',
  templateUrl: './package-attach-dialog.component.html',
  styleUrls: ['./package-attach-dialog.component.scss'],
})
export class PackageAttachDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<PackageAttachDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: PackageAttachDialog,
  ) {}

  public packageType = new FormControl('', [Validators.required, Validators.pattern(onlyNumbers)]);
  public rate = new FormControl('', [Validators.required, Validators.pattern(onlyNumbers)]);
  public type = new FormControl('', [Validators.required, Validators.pattern(packageAttachType)]);
  public quota = new FormControl('', [Validators.required, Validators.pattern(onlyNumbers)]);

  public cancel(): void {
    this.dialogRef.close();
  }
}
