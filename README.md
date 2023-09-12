# Exploratory NLST analysis of TotalSegmentator results

## Left and right region comparison

Bland-Altman and correlation plots of the left vs right regions, in terms of volume are [here](https://github.com/deepakri201/nlst_explore/tree/main/left_right_region_comparison/pdf). 

Bokeh plots for the ones that had outliers: 
- [Adrenal gland](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Adrenal%20gland.html)
- [Hip](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Hip.html)
- [Humerus](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Humerus.html)
- [Scapula](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Scapula.html)
- [First rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/First%20rib.html)
- [Second rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Second%20rib.html)
- [Third rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Third%20rib.html)
- [Fourth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Fourth%20rib.html)
- [Fifth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Eleventh%20rib.html)
- [Fifth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Adrenal\Fifth%20rib.html)
- [Sixth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Sixth%20rib.html)
- [Seventh rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Seventh%20rib.html)
- [Eighth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Eighth%20rib.html)
- [Ninth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Ninth%20rib.html)
- [Tenth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Tenth%20rib.html)
- [Eleventh rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Eleventh%20rib.html)
- [Twelfth rib](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/left_right_region_comparison/bokeh/Twelfth%20rib.html)

## Segmentation over time consistency 

Violin plots of the stddev of the volumes within each patient.  We expect for some organs that these deviations would be small over time. 

The pdf plots are [here](https://github.com/deepakri201/nlst_explore/tree/main/segmentation_over_time/pdf). 

The bokeh plots are here: 
- [Spleen](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/segmentation_over_time/bokeh/Spleen.html)
- [Liver](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/segmentation_over_time/bokeh/Liver.html)
- [L1 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/segmentation_over_time/bokeh/L1%20vertebra.html)
- [T7 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/segmentation_over_time/bokeh/T7%20vertebra.html)

## Organ volume comparison 

In this [folder](https://github.com/deepakri201/nlst_explore/tree/main/organ_volume_comparison), there is a csv file, where for each vertebrae, the min and max deviation compared to the median is provided along with the OHIF url. 

We can assess these outliers and compare the medians to literature. 

## Voxel volume vs mesh volume comparison (vertebrae for now)

Bland-Altman and correlation plots of the voxel volume vs mesh volume for the vertebrae [here](https://github.com/deepakri201/nlst_explore/tree/main/voxel_vs_mesh_volume_comparison/pdf). 

Bokeh plots for the ones that had outliers: 
- [C1 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/C1%20vertebra.html)
- [C5 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/C5%20vertebra.html)
- [C6 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/C6%20vertebra.html)
- [C7 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/C7%20vertebra.html)
- [T1 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T1%20vertebra.html)
- [T2 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T2%20vertebra.html)
- [T3 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T3%20vertebra.html)
- [T4 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T4%20vertebra.html)
- [T5 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T5%20vertebra.html)
- [T6 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T6%20vertebra.html)
- [T7 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T7%20vertebra.html)
- [T8 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T8%20vertebra.html)
- [T9 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T9%20vertebra.html)
- [T10 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T10%20vertebra.html)
- [T11 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T11%20vertebra.html)
- [T12 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/T12%20vertebra.html)
- [L1 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/L1%20vertebra.html)
- [L2 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/L2%20vertebra.html)
- [L4 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/L4%20vertebra.html)
- [L5 vertebra](https://htmlpreview.github.io/?https://github.com/deepakri201/nlst_explore/blob/main/voxel_vs_mesh_volume_comparison/bokeh/L5%20vertebra.html)
