# team_phyte_s_little_sytes one-shot
Decisions: wedge generator, short body (75 mm) behind a wide curved front wedge; photos show two copies, masks recut with --crop on one robot.
Likeness (robot likeness, one run): NOT MEASURED: likeness.mask_source rejects cropped masks (IoU 0.29/0.42/0.25 vs uncropped auto mask) because REFERENCE.json has no crop key and agents may not edit it.
Wrong vs photo: Wedge is flat, photo wedge is a wide curved scoop with raised side fins and a V-shaped rear top; no silhouette score obtained.
Would have helped: mask_source should honour the --crop used (or a crop field in the spec reference entry).
Renders: renders/iso.png, renders/top.png. Full likeness output: likeness.txt
