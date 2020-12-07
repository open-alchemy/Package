import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { OAuthModule } from 'angular-oauth2-oidc';

import { AppRoutingModule } from './app-routing.module';

import { AuthGuard } from './services/auth-guard.service';

import { AppComponent } from './app.component';
import { SpecsComponent } from './components/specs/specs.component';
import { SignInCompleteComponent } from './components/sign-in-complete/sign-in-complete.component';

@NgModule({
  declarations: [AppComponent, SpecsComponent, SignInCompleteComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    OAuthModule.forRoot(),

    MatProgressSpinnerModule,
  ],
  providers: [AuthGuard],
  bootstrap: [AppComponent],
})
export class AppModule {}
