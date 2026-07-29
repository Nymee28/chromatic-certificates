# Additif v2 au Recueil des théorèmes et lemmes
### Deux pièces nouvelles depuis l'envoi du recueil : le Théorème 3 (présentation finie de G_CH(q,4), module 4) et le Corollaire NC

*28 juillet 2026. Cet additif complète le recueil envoyé en relecture sans le modifier — conformément à la doctrine « donner petit à petit ». Conventions inchangées : [T-ℚ] démontré exact sur ℚ ; [C-p] computationnel modulo premiers concordants ; [L] lemme rédigé avec liste [R] ouverte ; [CONJ] conjecture. Les scripts et registres cités sont dans `5-laboratoire/`.*

---

## Théorème 3 — Présentation finie de G_CH(q,4) en module 4 — statut [T-ℚ pour q = 3…12 ; L pour tout q]

**Énoncé.** Pour tout q ≥ 3, le graphe circulant 5-critique G_CH(q,4) de Cameron–Hoàng (n = 4q+1) admet un certificat de Nullstellensatz exact sur ℚ de non-4-coloriabilité, de degré 5 (encodage racines quartiques, niveaux {1,5}), supporté sur les arêtes d'écart ≤ 3 et de forme éclaireur × gadget (rayon 3). La famille est capturée par un objet fini : 6 487 étiquettes indépendantes de n, 6 186 équations (fermées à partir de q = 10), et deux vecteurs de constantes rationnelles V_pair, V_impair (dénominateurs | 2⁴) tels que le certificat de G_CH(q,4), q ≥ 6, est l'instanciation de V_{q mod 2}. Les deux strates ont une cause arithmétique démontrée : ⌊n/2⌋ = 2q ≡ 0 ou 2 (mod 4).

**Preuve (composition).** Petits ordres q = 3, 4, 5 exacts individuels [T-ℚ] ; régime périodique q = 6…12 : sept solves exacts indépendants redonnant V_pair/V_impair bit à bit, trois prédictions directes vérifiées (0 équation violée sur 6 186, test de discrimination calibré) [T-ℚ] ; fermeture des équations : empirique (incréments nuls à q = 11 et 12, alphabet constant depuis q = 5) et structurelle (Lemme C-mod4 : fenêtres ≤ 10, saturation des types, invariance de zone générique par pas de 4, catalogue de bord antipodal fonction de q mod 2 seul ; seuil q₀ = 10) [L, liste R] ; instanciation par redistribution des constantes sur les colonnes, validée numériquement quatre fois jusqu'à 334 394 lignes. Pièces : `theoreme-1bis.md` (assemblage), `lemme-C-mod4.md` (fermeture), bilans CC-01/CC-02 (faits machine, reproduits bit à bit sur deux machines indépendantes).

**Trois lois inter-modules issues de la comparaison avec les Théorèmes 1 et 2** *(consignées comme faits, généralité [CONJ])* : écart minimal suffisant = k−1 (mesuré : 2 en module 3, 3 en module 4, les deux moitiés — insuffisance ET suffisance — établies à deux ordres chacune) ; strates de parité présentes dans les deux modules (cause démontrée en module 4) ; dénominateurs des présentations : 2·3² (module 3) et 2⁴ (module 4).

**Reproduction.** `python j2_labels.py 3 4 5 6 7 8 9 10 11 12` (checkpoints par premier, cache de build) ; `python j2_predict.py q` pour les prédictions ; `python j2_verify_joint.py` pour la descente aux colonnes.

---

## Corollaire NC — statut [conditionnel à la Conjecture d'effondrement]

**Énoncé.** Si la Conjecture d'effondrement est vraie (tout graphe P₈-free non-3-coloriable admet un certificat de degré ≤ 4), alors le problème « G P₈-free est-il 3-coloriable ? » est dans **NC²** : décidable par circuits uniformes de taille polynomiale et de profondeur O(log² n). Inconditionnellement : le test du degré 4 est lui-même dans NC², et la promesse P₈-free se teste en AC⁰.

**Preuve (pipeline).** (0) Test de promesse : OR de O(n⁸) prédicats locaux — AC⁰. (1) Construction du système de niveau {1,4} : O(n⁶) entrées, chacune calculable localement — NC¹ uniforme. (2) Solvabilité de Ax = e sur ℚ : rang(A) = rang([A|e]) ; le rang d'une matrice entière à coefficients bornés se lit sur les coefficients du polynôme caractéristique de AᵀA (semi-définie positive : le rang est l'indice du dernier coefficient non nul), calculé sans division par Berkowitz — NC² ; artillerie générale : Mulmuley, *Combinatorica* 1987 (rang sur tout corps en NC, source primaire vérifiée). (3) Composition : profondeur O(log² n), taille polynomiale. ∎ Pièce : `11-p-vs-nc/K3-certification-nc.md` (bornes fines par étage).

**Portée.** L'effondrement conjecturé ne placerait pas seulement 3-COL P₈-free dans P mais dans NC² — la classe des problèmes de profondeur polylogarithmique. Le mécanisme est celui, historiquement attesté, des chutes de P vers NC : remplacer la procédure de recherche par un invariant algébrique (déterminant, rang, matrice de Tutte — ici le rang d'un système de certificats). Contexte : la 3-coloration des Pₜ-free n'est NP-complète pour aucun t connu, la frontière polynomiale est ouverte à t = 8 ; la NP-dureté n'est donc pas l'obstacle — la profondeur non plus, si la Conjecture tient.

---

*Fin de l'additif v2. Les pièces complètes (démonstrations, tables des douze ordres, listes [R], journaux d'exécution) sont dans les dossiers 9 et 11 du projet.*
