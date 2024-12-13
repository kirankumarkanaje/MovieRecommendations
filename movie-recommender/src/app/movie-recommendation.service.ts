import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MovieRecommendationService {
  private apiUrl = 'http://localhost:5001/recommend'; // Update if your backend differs

  constructor(private http: HttpClient) { }

  getRecommendations(movies: string[]): Observable<any> {
    return this.http.post(this.apiUrl, { favoriteMovies: movies });
  }
}
