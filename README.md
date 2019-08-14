# MediocreAmateur
Where are the Mediocre Amateurs?

[MediocreAmateur](https://www.youtube.com/channel/UC-04mJDJUYHEyE8JPIEa0-w) is an  outdoor adventure YouTube channel featuring endurance athletes and beautiful footage. This project aims to build a more appealing listing of videos by showing geographic location of the adventures and some associated metadata.

## Technology

All site pages are hand written HTML; if other pages are added, I may roll a simple offline HTML templating.

Leaflet JS and OpenTopoMap are used to display map data.

The font "Dosis Bold" is used due to its similarity to the Mediocre Amateur font.

The Google API for YouTube is used to list all channel videos and get some video metadata.

## Deployment

### Production

The site is served as a static object on CloudFront, backed by an S3 bucket.

### Development

I've provided a simple Express JS server for delivering the site locally. To run it:

```bash
npm start --prefix server
```
