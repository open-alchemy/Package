import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './services/auth-guard.service';

import { SpecsComponent } from './components/specs/specs.component';
import { SignInCompleteComponent } from './components/sign-in-complete/sign-in-complete.component';

const routes: Routes = [
  { path: '', redirectTo: 'specs', pathMatch: 'full' },
  { path: 'specs', component: SpecsComponent, canActivate: [AuthGuard] },
  {
    path: 'sign-in-complete',
    component: SignInCompleteComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
