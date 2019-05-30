import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CompanySettingsComponent} from './company-settings.component';
import {urlValidator} from '../pattern';

describe('CompanySettingsComponent', () => {
  let component: CompanySettingsComponent;
  let fixture: ComponentFixture<CompanySettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CompanySettingsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CompanySettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeFalsy();
  });
});

describe('IntegrationComponentRegex', () => {
  const regex = new RegExp(urlValidator, 'g');

  const incorrectLinks = [
    'httpc//localhost.com/webhook',
    'htp/local:.com.web',
    'http/http.com/http',
    'htto://localhost.com/',
  ];

  it('should be incorrect link', () => {
    incorrectLinks.forEach(link => {
      expect(regex.test(link)).not.toBeTruthy();
    });
  });

  const correctLinks = [
    'http://localhost.com/webhook',
    'https://localhost.com/webhook',
    'http://localhost:8080/webhook',
    'https://localhost:8080/webhook',
    'http://localhost:1113/some-link/address',
    'http://localhost.ru:8080/webhook',
    'https://localhost.com:3000/webhook/1',
    'https://localhost:8080/',
    'https://localhost:8080/webhook/',
    'https://localhost:8080/some-link/address/',
  ];

  it('should be correct link', () => {
    correctLinks.forEach(link => {
      expect(regex.test(link)).toBeTruthy();
    });
  });
});
