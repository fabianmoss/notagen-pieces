# Experiment

## convert xml to wav 

```bash
for f in data/*.xml; do
    musescore "$f" -o "${f%.xml}.wav"
done
```

## format file lists for copying 

```bash 
```
```bash 
ls data/A | grep xml | sed 's|^|\"data/|; s|$|\",|'
```
```
```
```
```

## Todo

- Hören vom Bewerten trennen 
- Aktuelle Datein (tempi!)
- ? Wiederholung möglich? 
```

```
```
