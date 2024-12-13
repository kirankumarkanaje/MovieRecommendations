import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MovieRecommendationService } from '../movie-recommendation.service';

@Component({
  selector: 'app-movie-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './movie-form.component.html',
  styleUrls: ['./movie-form.component.scss']
})
export class MovieFormComponent {
  movieInputs: string[] = Array.from({ length: 10 }, () => '');
  recommendations: string[] = [];
  loading = false;
  error: string | null = null;

  constructor(private movieService: MovieRecommendationService) {}

  submit() {
    this.error = null;
    this.recommendations = [];
    const favoriteMovies = this.movieInputs.map(m => m.trim()).filter(m => m.length > 0);

    if (favoriteMovies.length === 0) {
      this.error = 'Please enter at least one movie.';
      return;
    }

    console.log(favoriteMovies)

    this.loading = true;
    this.movieService.getRecommendations(favoriteMovies).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
        this.loading = false;
        console.log(this.recommendations)
      },
      error: (err) => {
        console.error(err);
        this.error = 'An error occurred while fetching recommendations.';
        this.loading = false;
      }
    });
  }

  trackByIndex(index: number, item: string) {
    return index;
  }
}
