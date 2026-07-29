# Recueil des théorèmes, lois et résultats structurels
### Certificats de Nullstellensatz de degré borné pour deux familles infinies de graphes 4-vertex-critiques, lois génératrices explicites, et banc d'essai comparatif de trois ontologies de preuve
#### Programme « anomalies polynomiales » — cible n° 1 : la 3-coloration des graphes sans P₈. État consolidé au 21 juillet 2026.

---

*Nature de ce document : le recueil met à plat, avec leur statut épistémique précis, l'ensemble des énoncés que le programme peut aujourd'hui formaliser et soumettre. Chaque affirmation numérique est adossée à un registre machine reproductible (dossier `5-laboratoire/`, commandes en § 10). Convention de statut, utilisée partout :*

- ***[T-ℚ]** — théorème d'instance : vérifié exactement sur ℚ (arithmétique de fractions, zéro flottant, zéro modulaire) ;*
- ***[T mod R]** — théorème modulo rédaction : contenu machine-vérifié exhaustivement, argument mathématique rédigé en brouillon, étapes routinières restantes marquées [R] ;*
- ***[C-p]** — certifié modulaire : solvabilité établie mod ≥ 2 premiers concordants, avec certificat par résidu explicite (faux positif impossible) ; l'extraction exacte est mécanique mais non faite ;*
- ***[CONJ]** — conjecture, avec son support expérimental exact.*

*Garde-fou liminaire, répété en § 9 : rien dans ce recueil ne prétend toucher P vs NP. Les objets sont des « îlots » — des classes ouvertes, non connues NP-dures, où un résultat polynomial est réellement découvrable.*

---

## 1. Le cadre en cinq définitions

**(D1) Encodage par racines cubiques de l'unité** (Bayer). Pour un graphe G sur n sommets, on travaille dans R_n = ℚ[x₀, …, x_{n−1}]/(x_i³ − 1) ; à chaque arête e = {i, j} on associe g_e = x_i² + x_i x_j + x_j². Le système {g_e = 0} a une solution dans les racines cubiques si et seulement si G est 3-coloriable.

**(D2) Certificat de Nullstellensatz de degré d.** Une identité Σ_{e,m} μ(e,m) · m · g_e = 1 dans R_n, avec deg(m·g_e) ≤ d après réduction. Son existence prouve la non-3-colorabilité ; le degré minimal d_HN(G) mesure la taille de la preuve algébrique, et sa recherche à d fixé est de l'algèbre linéaire (dimension polynomiale en n) — parallélisable, de la classe NC. La graduation mod 3 de R_n impose deg(m) ≡ 1 (mod 3) : les degrés utiles sont 1, 4, 7, … Le premier étage non trivial est d = 4. (Généralisation en module k pour la non-k-colorabilité : x_i^k = 1, g_e = Σ_l x_i^{k−1−l} x_j^l, multiplicateurs ≡ 1 mod k, premier étage k+1.)

**(D3) Les deux familles infinies.** *(a)* **G(q,3)** (Pokrovskiy ; = cas k = 3 des G(q,k) de Cameron–Hoàng) : circulant sur n = 3q+1 sommets, écarts {1} ∪ {2+3j : j = 0…q−1} ; 4-vertex-critique, sans P₇ induit. *(b)* **G_ZJ(k)** (Zhou–Jooken–Shan–Goedgebeur–Huang) : circulant sur n = 3k+10 sommets, écarts {±1} ∪ {5+3j : j = 0…k} ; 4-vertex-critique et **sans triangle** pour k ≥ 3. Propriétés re-vérifiées par machine sur les premiers membres de chaque famille.

**(D4) Systèmes réduits.** Par symétrie cyclique, le système de certificats se quotiente par ℤ_n (lignes = monômes canoniques, colonnes = paires (arête, multiplicateur) canoniques). Fait structurel [T-ℚ de comptage, vérifié exhaustivement] : dans le système ansatz quotient de ZJ, toutes les entrées valent exactement n — d'où la normalisation ν = n·μ qui rend le système des classes indépendant de n (§ 3).

**(D5) Familles d'ansatz.** Le support des certificats est découvert expérimentalement puis fixé : pour G(q,3), arêtes d'écarts {1, 2}, multiplicateurs = « éclaireur » x_a seul ou éclaireur × gadget local (quatre formes et miroirs) ; pour ZJ, arêtes d'écarts {1, 5, 8} (chaque sous-ensemble propre échoue — la rigidité est testée), fenêtre W = 4. Les systèmes restreints sont de taille O(n).

---

## 2. Théorème 1 — la famille de Pokrovskiy : degré exactement 4, loi fermée à 77 constantes

> **Théorème 1** *(statut : **[T-ℚ]** pour 22 instances jusqu'à n = 151 ; **[T mod R]** pour « tout q », via le Lemme L).* Il existe une table explicite de 77 constantes rationnelles {c(κ)}, toutes de dénominateur divisant 18, indexées par des clés de zone (TÊTE : 19 constantes, forme complète ; CŒUR : 14, clé (écart, gadget, distance mod 3) ; BORD : 44, clé (écart, gadget, distance à l'antipode ≤ 4, parité de n)), telle que pour tout q ≥ 1, l'assignation μ = c(κ)/n est un certificat de Nullstellensatz de degré 4 de la non-3-colorabilité de G(q,3).
>
> **Corollaire.** Le degré de Nullstellensatz de la famille infinie {G(q,3)} est exactement 4 (pas de certificat de degré 1 — vérifié à chaque étage ; degrés 2, 3 exclus par graduation). À notre connaissance, premier résultat de bornitude uniforme de certificats de Nullstellensatz sur une famille infinie de graphes 4-vertex-critiques.

**Comment la loi a été trouvée** : extraction exacte des petits membres (CRT + reconstruction rationnelle + vérification sur ℚ) → alignement des coefficients ×n sur les formes → liage par clés de zone (système « macro » ~150 colonnes) → **empilement** des systèmes macro q = 6…12 sur variables partagées (2 058 × 206, résolu en 10 s) → la solution unique **génère sans résolution** tous les q testés ensuite.

**Registre [T-ℚ]** : q = 1…17 consécutifs + 20, 25, 30, 40, 50 (n = 4 → 151) — les q ≥ 13 générés par la table seule, puis vérifiés exactement. **Architecture du Lemme L [T mod R]** (`preuve-lemme-L.md`) : équivariance diédrale (A), localité des produits (B), classification des équations en quatre types (C), stratification — n ≡ 1 mod 3 toujours, donc tout dépend de la seule parité de q, deux strates —, réalisation et disjonction (D), vérification finie (faite : douze q consécutifs couvrent deux fois toutes les classes des deux strates). **Contrôle machine** : q = 16 vs 18 — 270/270 classes stables ; q = 17 vs 19 — 265/265 ; zéro incohérence, zéro orpheline. Restent les tabulations [R] (une vingtaine de cas mécaniques) et la relecture humaine (~200 lignes d'arithmétique de fractions).

---

## 3. Théorème 2 — la famille sans triangle ZJ : degré 4 partout, et la loi un étage au-dessus

> **Théorème 2** *(statut : **[T-ℚ]** pour k = 3…8 et pour les témoins k = 32, 33 ; **[C-p]** pour k = 9…31 ; **[T mod R]** pour les queues infinies des deux strates, via les Lemmes N, C-ZJ, I).* Pour tout k ≥ 3, la non-3-colorabilité de G_ZJ(k) admet un certificat de Nullstellensatz de degré 4. Explicitement : il existe deux tables de constantes rationnelles ν_paire (2 377 valeurs non nulles) et ν_impaire (2 408 valeurs), toutes de dénominateur divisant 216 = 2³·3³, indexées par des étiquettes de formes indépendantes de n, telles que μ = ν(étiquette)/n est un certificat de degré 4 pour tout k ≥ 32 de la strate de parité correspondante.

**Le fait remarquable — où vit la loi.** Les certificats-représentants canoniques de ZJ n'obéissent à *aucune* loi par clé de forme : sur 445 clés communes aux six membres exacts, 444 ne suivent ni constante, ni a+b/n, ni a+b/n+g/n², ni forme rationnelle (a+bn)/(g+dn) — et la stratification par parité ne sauve rien (1/505 et 5/644). La loi existe pourtant, **un étage au-dessus** : dans le *quotient*. En variables ν = n·μ (légitimées par le facteur d'orbite uniforme, § 1 D4), le système fini des étiquettes est rigoureusement indépendant de n, et il est résoluble. La paire {négative des représentants, positive du quotient} est la leçon structurelle du pilier : *le bon étage d'uniformité d'une famille ne se décrète pas, il se cherche*.

**Architecture de la preuve** (`preuve-lemmes-ZJ.md`) : **Lemme N** (normalisation — le facteur d'orbite n, vérifié 303 591/303 591 entrées à k = 20) ; **Lemme C-ZJ** (classification et stabilité — étiquettes diédrales invariantes testées 0 échec/8 000, zones à marge de couture *mesurée* (maximum 12), saturation à n ≥ 104) ; **Lemme I** (instanciation — trois lignes : la signature de chaque ligne est l'équation de sa classe, ν satisfait toutes les classes, donc μ = ν/n satisfait le système à tout n saturé).

**Contrôle machine de C-ZJ** (l'échelle ×300 du contrôle du Lemme L) : strate paire, k = 32 vs 34 (n = 106/112) — **81 920/81 920 classes stables, 0 incohérence, 0 orpheline** ; strate impaire, k = 33 vs 35 (n = 109/115) — **82 833/82 833, 0, 0** ; menus d'étiquettes de colonnes identiques (38 670 = 38 670 ; 39 522 = 39 522).

**Existence et exactitude de ν [T-ℚ]** : systèmes des étiquettes 33 429 × 38 670 et 34 132 × 39 522 ; solvabilité par Wiedemann creux à résidu certifié (2 premiers/strate) ; extraction par RREF uint8 six premiers + CRT + reconstruction rationnelle ; vérification exacte du système sur ℚ (fractions) ; et **l'étalon-or** — l'instanciation vérifiée par re-expansion polynomiale complète aux témoins saturés : **G_ZJ(32), n = 106 : exact** ; **G_ZJ(33), n = 109 : exact**.

**Couverture k = 3…31** : certificats exacts sur ℚ pour k = 3…8 (dont le « membre du mur » k = 8) [T-ℚ] ; balayage k = 9…31 par Wiedemann à résidu certifié, **23/23 solvables** [C-p]. **[R] restants** : inventaire des décompositions, bijection de transport, stabilisateurs, bornes inférieures systématiques sur les 29 membres individuels.

**Portée** : la famille ZJ est sans triangle — l'effondrement de degré tient donc dans la zone aveugle du SDP (§ 5) et au-delà de la classe P₈-free d'origine.

---

## 4. Résultats structurels annexes (chacun avec registre)

**4.1 Rigidité du support {1, 5, 8}** *(ZJ ; [C-p], testé k = 3, 4, 5)* : le système ansatz est solvable sur les arêtes d'écarts {1, 5, 8} et échoue sur chaque sous-ensemble propre ; les autres écarts sont inutiles. Le support des certificats est un invariant de la famille.

**4.2 La mort des lois de représentants** *(ZJ ; [T-ℚ], six certificats exacts à canonicalisation partagée)* : verdict D3 final ci-dessus (444/445). Établi sur les représentants RREF variables-libres-nulles ; c'est une propriété du choix de représentant, démontrée compatible avec l'existence de la loi de quotient (§ 3).

**4.3 Spectroscopie des dénominateurs.** *(a)* **Platitude ansatz [T-ℚ]** : dans les six certificats ansatz exacts (k = 3…8, n = 19…34), la partie impaire de n apparaît à la puissance exactement 1 : 19¹, 11¹, 5² (= 25¹), 7¹, 31¹, 17¹ — histogrammes de valuations complets, aucune exception. *(b)* **H-parité des plein-systèmes [observation, 3 points]** : les représentants plein-système portent ⟨partie impaire de n⟩² si n est pair (11² dans 4 284 coefficients à n = 22), ⟨n⟩¹ si n est impair — la profondeur est une propriété du représentant, pas de l'instance. *(c)* Les lois trouvées ont des dénominateurs bornés indépendants de n : | 18 (T1), | 216 (T2).

**4.4 Le mur requalifié** *(ZJ ; [T-ℚ])* : l'échec d'empilement des lois macro à k = 8 (constaté en campagne) était un mur de *loi de représentants*, pas de *degré* ni de *support* — le certificat exact de ZJ(8) existe avec le même ansatz que les autres membres.

**4.5 Pilier 3 — la 4-coloration** *(G(q,4) de Cameron–Hoàng, 5-critiques ; [C-p])* : G(2,4), G(3,4), G(4,4) certifiés au niveau 5 — le premier étage au-dessus du minimum dans la graduation mod 4. Le motif « degré = premier étage autorisé » n'est pas propre à la 3-coloration.

**4.6 Le corpus d'obstructions** : 2 630 graphes 4-vertex-critiques énumérés (tous à ≤ 10 sommets + sans-triangle ≤ 13) ; 69/69 instances testées ont un certificat de degré 4 [T-ℚ pour les extraits, C-p pour le reste] ; premières obstructions à P₈ induit exactement à n = 10 ; aucune ≤ 10 ne contient 2P₄.

---

## 5. Le banc d'essai des trois ontologies — un même corpus, trois manières de « voir »

Sur le même corpus (les 36 obstructions 4-critiques sans-triangle ≤ 13 sommets + contrôles + les familles), trois familles de méthodes de certification de χ ≥ 4 ont été confrontées. À notre connaissance, ce banc d'essai triple n'existe pas dans la littérature.

| Ontologie | Instrument | Sporadiques sans-triangle (36) | Familles circulantes | Contrôles |
|---|---|---|---|---|
| **Continue** | SDP de coloration vectorielle + borne de Hoffman | **0/36** (toutes trompées : χ_vect ≈ 3) | aveugle (sans-triangle) | 435/477 du corpus général attrapées |
| **Topologique** | Homologie du complexe de voisinage (borne de Lovász) ; obstruction équivariante du complexe-boîte (test d'application de chaînes ℤ₂ → S¹ sur GF(2)) | **31/36** — toutes des **sphères d'homologie** (H̃₀ = H₁ = 0, H₂ = ℤ, sans torsion) ; 5 échappées (b₁ ≥ 1, et test boîte muet) | **0** — les onze membres testés (ZJ(3…8), G(2…6,3)) sont des **cercles d'homologie** (H̃₀, H₁, H₂) = (0, ℤ, 0), et l'obstruction équivariante est muette | 5/5 conformes (K₄, Grötzsch certifiés ; C₅, C₇, Petersen muets) |
| **Algébrique** | Certificats de Nullstellensatz degré 4 (NulLA) | **36/36** | **toutes, uniformément** (Théorèmes 1 et 2) | conformes (pas de certificat pour les 3-coloriables) |

**Lectures.** *(i)* La hiérarchie est stricte : continu ⊊ topologique ⊊ algébrique sur ce corpus. *(ii)* La dichotomie topologique est nette et inattendue : sporadiques → sphères (le « trou qui interdit la coloration » existe littéralement, et c'est le même dans les 31 cas) ; circulants → cercles (le 1-cycle survivant est la structure cyclique du graphe, et il n'aide pas). *(iii)* Les cinq « échappées » — invisibles au continu, à la connexité *et* à l'obstruction équivariante testée, mais certifiées au degré 4 — sont les instances les plus discriminantes connues du corpus. *(iv)* Statuts : SDP [vérifié numériquement, solveur SCS] ; topologie [T-ℚ : SNF exacte sur ℤ pour les petits, mod 2 premiers concordants pour les grands ; caveat : « ACTIVE » = condition nécessaire de 1-connexité, π₁ non calculé ; variante exacte de complexe-boîte à collationner] ; algèbre [statuts du § 2–3].

---

## 6. La méthode, en tant que méthode

La chaîne qui a produit les deux théorèmes est identique aux deux étages et se veut réutilisable :

1. **Découverte de support** : solvabilité à support restreint, élagage jusqu'à rigidité (D5).
2. **Extraction exacte** : solutions mod plusieurs premiers, pivots concordants, CRT, reconstruction rationnelle, **vérification exacte sur ℚ** — jamais de proxy modulaire dans un énoncé final.
3. **Étiquetage indépendant de n** : formes locales exactes + zones périodiques (mod 3) + coutures à marge *mesurée* + pliage diédral — et contrôle d'invariance par tirages aléatoires.
4. **Contrôle de stabilité** : cohérence intra-n et stabilité inter-n des classes d'équations, aux tailles saturées, par strate.
5. **Le système fini** : loi cherchée dans le quotient (ν = n·μ), solvabilité certifiée par résidu, extraction exacte, **témoins vérifiés à l'étalon-or**.
6. **Réduction du « pour tout n » à du fini** : lemmes de transport (gabarit Lemme L), vérifications finies couvrantes, annexes machine.

Ingénierie de calcul (conforme, incidemment, à une algorithmique des « qualités du matériel » — flots réguliers, arithmétique exacte à mots courts) : élimination par blocs BLAS à réduction différée (16×) ; **Wiedemann creux sur équations normales implicites** (mémoire ÷ 100-203, verdicts SOLVABLE certifiés par résidu — faux positif impossible) ; RREF **uint8** à premiers 8 bits, panneaux float32 exacts ; checkpoints par premier. Le tout sur une machine de 8 Go.

---

## 7. Table des statuts (le contrat de lecture)

| Énoncé | Statut | Registre |
|---|---|---|
| T1 sur 22 instances (n ≤ 151) | **[T-ℚ]** | `resultats/certificats/`, `common_law.json` |
| T1 pour tout q (Lemme L) | **[T mod R]** | `preuve-lemme-L.md`, `annexe-classes-lemmeL.md`, stabilité 270+265 |
| T2 pour k = 3…8 | **[T-ℚ]** | `zj_ansatz_results.json` (6 certificats) |
| T2 pour k = 9…31 | **[C-p]** | `zj_gap_results.json` (23/23, résidus) |
| T2 témoins k = 32, 33 | **[T-ℚ]** | `zj_nu_k34.json`, `zj_nu_k35.json` |
| T2 queues infinies | **[T mod R]** | `preuve-lemmes-ZJ.md`, stabilité 81 920 + 82 833 |
| Bornes inférieures (pas de degré 1) | [T-ℚ]/[C-p] selon membre | registres par famille |
| Mort des lois de représentants (D3) | **[T-ℚ]** | `zj_final_diag.json` (444/445) |
| Platitude ansatz (valuations) | **[T-ℚ]** | histogrammes, 6 certificats |
| Hiérarchie des ontologies | mixte (voir § 5 iv) | `lab_sdp.json`, `topo_*.json` |
| Pilier 4-coloration (niveau 5) | **[C-p]** | `pillar_results.json`, `sparse_results.json` |
| Conjecture d'effondrement P₈ (toute la classe) | **[CONJ]** | 69/69 + T1 + T2 ; aucune borne inférieure connue ne touche la classe (les familles dures de la littérature contiennent toutes de longs chemins induits) |

---

## 8. Ce que ces résultats visent (le programme), et ce qu'ils ne prétendent pas

**Le programme.** La 3-coloration des graphes sans P₈ est la seule ligne ouverte de la grille (k couleurs, Pₜ interdit) : quasi-polynomiale connue, dureté improbable, polynôme recherché. La **Conjecture d'effondrement** — d_HN uniformément borné (= 4 ?) sur les P₈-free non-3-coloriables — impliquerait 3-COL P₈-free ∈ P par pure algèbre linéaire. Les Théorèmes 1 et 2 en sont les deux premiers piliers durs : deux familles infinies critiques, l'une P₇-free, l'autre sans triangle, à degré exactement 4, avec lois génératrices explicites — et le § 4.5 suggère que le phénomène traverse les modules.

**Les garde-fous.** (1) Rien ici n'approche P = NP ; un îlot gagné est un théorème publiable, pas une révolution. (2) Les statuts du § 7 sont le contrat : aucun [C-p] n'est présenté comme un théorème d'instance, aucun [T mod R] comme achevé. (3) Deux vérités expérimentales ne font pas une asymptotique : la Conjecture reste une conjecture, et le volet « réfutation » (encoder les gadgets durs de la littérature sans longs chemins induits) reste au programme. (4) Les définitions topologiques (variante de complexe-boîte) et quelques attributions sont signalées « à collationner sur sources primaires » avant publication — la charte du dossier depuis la leçon Clickomania.

---

## 9. Reproduction

Dépendances : Python ≥ 3.11, numpy (+ cvxpy/SCS pour le volet SDP, nauty pour régénérer le census). Dossier `5-laboratoire/`.

```
# Théorème 1
python3 macro_law.py common            # loi 77 constantes : résolution empilée + générateur held-out
python3 stability_check.py             # contrôle Lemme L : 270/270, 265/265
# Théorème 2
python3 zj_ansatzcert.py 4 3 4 5       # certificats exacts petits membres (W=4)
python3 zj_transfer_check.py dump 32 && python3 zj_transfer_check.py dump 34 \
  && python3 zj_transfer_check.py cmp 32 34    # stabilité strate paire : STABLE
python3 zj_label_solve.py 34           # solvabilité du système des étiquettes (résidu)
python3 zj_nu_extract.py 34 32         # extraction exacte de ν + témoin étalon-or
python3 zj_gap_sweep.py                # balayage k=9..31 (reprise automatique)
# Banc d'essai des ontologies
python3 run_lab.py L4small && python3 continuous.py   # algèbre + SDP
python3 topo_lab.py && python3 topo_families.py && python3 topo_box.py  # topologie
```

*Annexe de fichiers : les preuves (`preuve-lemme-L.md`, `preuve-lemmes-ZJ.md`), le rapport de campagne (`rapport-campagne-piliers.md`), les registres JSON cités, et le dossier de relecture court (`dossier-relecture-lemmeL.pdf`) pour l'entrée en matière.*
