import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';

import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { OAuthModule } from 'angular-oauth2-oidc';
import { SpecsService, SpecService } from '@open-alchemy/package-sdk';

import { AppRoutingModule } from './app-routing.module';

import { AuthGuard } from './services/auth-guard.service';
import { packageReducer } from './services/package/package.reducer';
import { PackageEffects } from './services/package/package.effects';

import { AppComponent } from './app.component';
import { SpecsComponent } from './components/specs/specs.component';
import { SignInCompleteComponent } from './components/sign-in-complete/sign-in-complete.component';
import { SpecsTableComponent } from './components/specs-table/specs-table.component';

@NgModule({
  declarations: [
    AppComponent,
    SpecsComponent,
    SignInCompleteComponent,
    SpecsTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    OAuthModule.forRoot(),

    StoreModule.forRoot({ package: packageReducer }),
    EffectsModule.forRoot([PackageEffects]),

    MatProgressSpinnerModule,
    MatTableModule,
  ],
  providers: [
    AuthGuard,
    { provide: SpecsService, useValue: new SpecsService() },
    { provide: SpecService, useValue: new SpecService() },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
