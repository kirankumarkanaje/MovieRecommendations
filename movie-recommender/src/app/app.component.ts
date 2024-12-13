import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MovieFormComponent } from './movie-form/movie-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MovieFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'movie-recommender';
}
