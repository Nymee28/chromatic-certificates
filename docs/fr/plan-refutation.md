# Dossier 10 — Le plan de réfutation
### Chantier 2 : l'attaque adverse contre la Conjecture d'effondrement au degré 4

*Document de travail, 22 juillet 2026. Convention de statuts du recueil : [T-ℚ] démontré exact, [C-p] computationnel modulo premiers concordants, [CONJ] conjecture.*

---

## 1. Pourquoi chercher à réfuter

Toutes nos preuves en faveur de la Conjecture d'effondrement (« tout graphe P₈-free non-3-coloriable admet un certificat de Nullstellensatz de degré ≤ 4 ») sont de forme confirmatoire : le census exhaustif aux petits ordres, les 36 sporadiques, les deux familles infinies (G(q,3), ZJ) avec leurs théorèmes. Une conjecture n'acquiert de la valeur qu'en survivant à des attaques construites pour la tuer. Ce dossier est l'attaque : trois expériences conçues pour produire une **graine de réfutation** — une instance P₈-free non-3-coloriable dont le système complet de degré 4 est INSOLVABLE — ou, à défaut, pour comprendre structurellement pourquoi on n'en trouve pas.

## 2. L'argument structurel : pourquoi les machines à bornes inférieures connues ne s'appliquent pas

C'est le résultat théorique du chantier, simple mais décisif pour situer la Conjecture.

**Lemme D (diamètre).** Tout graphe connexe P₈-free a un diamètre ≤ 6.
*Preuve.* Un plus court chemin entre deux sommets à distance d est un chemin induit à d+1 sommets. S'il existait deux sommets à distance ≥ 7, il existerait un chemin induit à ≥ 8 sommets, contredisant la P₈-liberté. ∎

(On peut toujours se ramener au cas connexe : un graphe non-3-coloriable a une composante connexe non-3-coloriable, elle-même P₈-free.)

**Corollaire M (Moore).** Si G est connexe d'ordre n, de degré maximal Δ et de diamètre ≤ 6, alors n ≤ 1 + Δ + Δ(Δ−1) + … + Δ(Δ−1)⁵, donc **Δ = Ω(n^{1/6})** : toute famille infinie P₈-free connexe est de degré non borné. ∎

**Conséquence.** Toutes les bornes inférieures de degré connues pour le Nullstellensatz et le Polynomial Calculus sur la coloration — Lauria–Nordström sur les graphes aléatoires épars G(n, d/n), les arguments de type Tseitin sur expandeurs, et en général toute la machinerie « expansion des petits ensembles » — vivent sur des graphes **épars à degré borné**, dont les chemins induits sont longs par construction (la maille et l'expansion les garantissent). La P₈-liberté interdit structurellement ce territoire : *les instances dures connues ne peuvent pas être importées dans notre classe*. Deux lectures :

- **Optimiste** : la Conjecture habite une zone où aucune arme de borne inférieure existante ne porte. Ce n'est pas un hasard si l'effondrement y est possible — la densité locale forcée (Δ ≥ c·n^{1/6}) fournit mécaniquement beaucoup de générateurs d'arêtes par sommet, la matière première des certificats bas degré.
- **Prudente** : c'est un argument de **non-réfutabilité-par-import**, pas une preuve. Une réfutation native — construite directement dans le territoire dense — reste concevable. D'où les expériences ci-dessous.

## 3. Les trois expériences (+ un raffinement)

### (i) La chasse à la frontière — EN COURS

Générer des graphes aléatoires G(n, p), p ∈ [0.30, 0.50], aux ordres n = 14, 15, 16 — **au-delà de la portée du census** (10 en général, 13 sans triangle) : territoire jamais exploré, donc test *hors échantillon* de la Conjecture (formée sur n ≤ 13 + familles). Filtres exacts : χ ≥ 4 (backtracking) puis P₈-free (plus long chemin induit < 8). Curation : les 25 plus épars (proches de la criticité en arêtes, là où le degré 4 a le moins de matière) + 15 étalés en densité. Test : **système complet** de niveau {1, 4} (tout le support des multiplicateurs), Wiedemann creux certifié par résidu, deux premiers concordants.

Fait notable déjà acquis : à n = 14, **1 846 candidats sur 4 000 tirages** — la classe P₈-free non-3-coloriable n'est pas mince à cette taille. La Conjecture couvre un territoire gras, et la chasse l'échantillonne honnêtement.

### (ii) La densification — l'import forcé des instances dures

L'expérience duale de l'argument du §2. Prendre une instance dure au sens de Lauria–Nordström (graphe épars non-3-coloriable à longs chemins induits), puis **tuer ses P₈ par ajout de cordes** : tant qu'il existe un chemin induit à 8 sommets, ajouter une corde qui le brise (stratégies : corde aléatoire sur le chemin trouvé ; corde minimisant l'accroissement de degré). L'ajout d'arêtes préserve χ ≥ 4 ; le point d'arrivée est P₈-free par construction. Mesurer : le nombre de cordes nécessaires, le degré maximal final, et **le verdict du degré 4 avant/après**. Prédiction de la Conjecture : la densification fait s'effondrer le degré à ≤ 4. Si l'on trouve une trajectoire de densification qui reste insolvable au degré 4 une fois P₈-free — graine de réfutation. Script : `densify.py`.

### (iii) Le protocole de vérification d'une graine

Toute instance signalée INSOLVABLE au degré 4 déclenche, avant toute annonce : (1) concordance sur ≥ 5 premiers indépendants (l'insolvabilité mod p pour p aléatoire n'échoue que sur les premiers divisant certains mineurs — finiment nombreux) ; (2) tentative de réfutation de la réfutation : recherche exacte d'un certificat sur ℚ par reconstruction rationnelle ; (3) si la graine tient : test au niveau 7 (le degré suivant ≡ 1 mod 3) — une graine insolvable au degré 4 mais solvable au degré 7 réfute la Conjecture *telle quelle* mais sauve une version affaiblie (degré ≤ 7) ; insolvable aux deux, elle attaque le programme entier. Charte : aucune annonce sans les étapes (1)-(2).

### (iv) Raffinement : la criticalisation

Parmi les candidats, extraire les **cœurs critiques dans la classe** : retirer une arête e tant que χ(G−e) ≥ 4 **et** G−e reste P₈-free (le retrait d'arêtes peut créer des chemins induits — la double condition est nécessaire). Le point fixe est une instance « arête-critique dans P₈-free » : le noyau dur minimal, là où une montée de degré se verrait en premier. Dédoublonner les cœurs, tester ceux qui échappent à la curation (i). Script : `criticalize.py`.

## 4. Portée honnête de chaque verdict

- **Système complet, niveau {1,4}** : la solvabilité équivaut exactement à l'existence d'un certificat de degré ≤ 4 (la graduation ≡ 1 mod 3 fait des niveaux 1 et 4 le support intégral). C'est *le* test de l'énoncé de la Conjecture — contrairement aux ansatz restreints (zones, étiquettes), qui ne témoignent que dans un sens.
- **SOLVABLE sur 2 premiers concordants** = [C-p] : quasi-certitude (une divergence ℚ/mod p exigerait que les deux premiers divisent le même défaut de mineur), pas un théorème. L'extraction exacte sur ℚ met à niveau [T-ℚ] si une instance devient un objet de publication.
- **INSOLVABLE sur 2 premiers** = alerte, jamais une annonce : protocole (iii) obligatoire.
- **Absence de graine après k instances** : évidence d'échantillonnage, pas une preuve — mais chaque solvable à n ≥ 14 est un point *hors échantillon* que la Conjecture n'avait pas le droit de prédire et qu'elle prédit.

## 5. Résultats

### (i) Chasse n = 14 — COMPLET : 40/40 SOLVABLES [C-p]

Graine 20260722, 4 000 tirages, **1 846 candidats**, 40 retenus (20 à 49 arêtes). **40/40 solvables au degré 4**, système complet, deux premiers concordants. Systèmes 19 656–19 930 lignes × 43 960–107 702 colonnes, 26–186 s par instance. Zéro graine de réfutation. Premier test hors échantillon de la Conjecture (formée sur n ≤ 13 + familles) : elle prédit juste sur les 40 points. Détail : `resultats/refute_hunt_n14.json`.

### (iv) Criticalisation n = 14 — COMPLET : 30/30 SOLVABLES [C-p]

Les 1 846 candidats rabotés au point fixe sous la double condition → **624 cœurs distincts** (invariant grossier), 26,3 arêtes rasées en moyenne, cœurs de 6 à 33 arêtes. 75/624 d'ordre effectif ≤ 10 (déjà couverts par le census) ; **549 cœurs à ≥ 11 sommets effectifs, territoire neuf**. Les 30 plus épars testés : **30/30 solvables** (16 à 19 arêtes, 10–19 s par instance — les systèmes épars sont rapides).

**Découverte structurelle au passage** : des cœurs à 16 arêtes sur ≥ 11 sommets effectifs sont *sous* la borne des graphes 4-critiques (min degré 3 ⟹ ≥ ⌈3k/2⌉ = 17 arêtes à k = 11) — ils ne sont donc **pas** 4-critiques comme graphes. Leur structure : un petit moteur chromatique (un sous-graphe 4-critique d'ordre ≤ 10, souvent K₄) + des arêtes d'échafaudage dont l'unique rôle est de tuer des chemins induits. Dans la classe, ces arêtes sont **porteuses** : on ne peut pas les retirer sans créer un P₈. C'est la « criticité relative à la classe », un objet qui n'existait pas dans notre corpus, et le candidat naturel pour toute future tentative de réfutation fine. Détail : `resultats/critical_cores_n14.json`.

### (ii) Densification n = 14 — COMPLET : mécanisme mesuré, zone discriminante au-dessus [C-p]

10 instances éparses (21–35 arêtes, χ ≥ 4, **avec** P₈ induit — hors classe), 2 stratégies de cordes chacune. Résultats :

- **Les 10 instances « avant » sont déjà solvables au degré 4.** L'effondrement n'est pas une spécificité P₈-free aux petits ordres : à n = 14, il est universel, dans la classe et hors d'elle. Les bornes inférieures de Lauria–Nordström sont *asymptotiques* — elles ne mordent pas encore ici. Conséquence honnête : à cette taille, la densification ne peut pas observer de basculement INSOLVABLE→SOLVABLE ; la zone discriminante (où le hors-classe décroche pendant que la classe s'effondre — le contenu réel de la Conjecture) est au-dessus de notre frontière de calcul actuelle.
- **Le mécanisme est mesuré et il est bon marché** : tuer *tous* les P₈ coûte +1 à +13 cordes (médiane ~5), et le degré maximal croît de **0 ou 1** (0 systématiquement en stratégie mindeg). La pression de Moore (Δ ≥ c·n^{1/6}) est invisible à n = 14 (n^{1/6} ≈ 1,55) — cohérent avec l'argument du §2, qui est asymptotique lui aussi.
- 20/20 trajectoires densifiées (P₈-free) solvables — 20 points de plus pour la Conjecture, sur des instances *construites* et non tirées. Détail : `resultats/densify_n14.json`.

### (i) Chasse n = 15 — COMPLET : 40/40 SOLVABLES [C-p]

Graine 20260723, 4 000 tirages, **1 333 candidats**, 40 retenus (21 à 57 arêtes). **40/40 solvables au degré 4**, systèmes 29 026–29 331 × 68 400–162 450, 108–432 s par instance. Zéro graine. Détail : `resultats/refute_hunt_n15.json`.

### (i) Chasse n = 16 — COMPLET : 18/18 SOLVABLES [C-p]

Graine 20260724, 4 000 tirages, **877 candidats**, 18 retenus (30 à 63 arêtes). **18/18 solvables au degré 4**, systèmes jusqu'à **42 129 × 229 068** (les plus gros systèmes complets jamais résolus par le laboratoire), 380–1 840 s par instance. Zéro graine. La courbe d'abondance 1 846 → 1 333 → 877 (n = 14, 15, 16 ; mêmes 4 000 tirages, même fenêtre p) est elle-même une donnée : la classe s'amincit doucement dans cette fenêtre de densité, sans s'éteindre. Détail : `resultats/refute_hunt_n16.json`.

### (i) Chasse n = 17 — COMPLET : 12/12 SOLVABLES [C-p]

Graine 20260725, 4 000 tirages, **618 candidats**, 12 retenus (40 à 71 arêtes). **12/12 solvables au degré 4**, systèmes jusqu'à **59 229 × 324 683**, 22–51 min par instance. Zéro graine. Courbe d'abondance complète : 1 846 → 1 333 → 877 → 618 (n = 14…17). Détail : `resultats/refute_hunt_n17.json`.

### Bilan cumulé du chantier (22–23 juillet)

**170 verdicts, 170 conformes à la Conjecture, zéro graine** : 40 (chasse n=14) + 30 (cœurs critiques) + 30 (densification : 10 épars hors classe + 20 trajectoires densifiées) + 40 (chasse n=15) + 18 (chasse n=16) + 12 (chasse n=17). Tous en système complet {1,4}, deux premiers concordants [C-p]. La Conjecture a désormais prédit juste sur **quatre ordres entiers hors échantillon** (14, 15, 16, 17 — elle fut formée sur n ≤ 13 + familles), sur les cœurs minimaux de la classe, et sur des instances construites adversarialement. Au-delà de n = 17, le coût par instance (~1 h) rend la chasse aléatoire moins rentable que les attaques structurées (densification à grand n, familles LN tronquées) — à arbitrer.

## 6. Reproduction

```
python3 refute_hunt.py 14 4000 20260722     # chasse (i) : génération, curation, tests
python3 criticalize.py 14                   # raffinement (iv) : cœurs critiques
python3 densify.py                          # expérience (ii) : import forcé LN
```

Dépendances laboratoire : `census.py` (χ exact, chemins induits, graph6), `sparse_wiedemann.py` (solvabilité certifiée par résidu, multi-premiers).

## 7. Place dans le programme

Ce chantier est le versant falsificationniste du dossier 9 : si la Conjecture survit ici, sa reformulation comme énoncé de présentation finie (« P₈-free = union finie de schémas présentables + résidu fini ? ») hérite de la confiance accumulée ; si une graine apparaît, c'est le dossier 9 qui fournit le langage pour dire *où* la présentation casse (le résidu grossit, ou un schéma manque). Dans les deux cas, le travail sert.
