# Applicazione demo


## Come effettuare il bake dell'immagine

Posizionarsi nella cartella dove è presente il Dockerfile

esguire

```bash
podman build -t app:tag .
```

## Pubblicazion dell'immagine nel registry privato

1. login nel registry

    `podman login registry`

2. Tag the image.

    `podman tag app:tag registry/samples/app:tag`

3. Push the image to the private image registry.

    `push push registry/samples/app:tag`

## Lanciare l'immagine in locale (facoltativo)

```bash
podman run --name applicazione-demo -p 9043:9043 -p 9443:9443
```
