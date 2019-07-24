
#functions----------------------------
define timeStamp
	@echo $(2) "`date -u`" >> $(1)
endef
#-------------------------------------

#code options-------------------------
PYTHON = \python3
PYTHON_OPTS = -W ignore
#-------------------------------------

#folders------------------------------
_6 := ../_6_TLGs
#-------------------------------------

LOG := manuscript.log

$(LOG): main.pdf
	$(call timeStamp,$(LOG),"generated manuscript")

main.pdf: $(_6)/_G/fig1_conceptDiagram/fig1_conceptDiagram.pdf\
	  $(_6)/_G/fig2_logScoresFor20102011Training/fig2_logScoresFor20102011Training.pdf\
	  $(_6)/_G/fig3_triPlot/fig3_triPlotSeason_2017_2018.pdf\
          $(_6)/_G/fig4_logScoreGrid/fig4_logScoreGrid.pdf\
          $(_6)/_G/fig5_pairedDifferenceInLogScores/fig5_pairedDifferenceInLogScores.pdf\
          $(_6)/_G/fig6_logScoresByEpidemicWeek/fig6_logScoresOverEpidemicWeeks.pdf\
          $(_6)/_G/fig7_setOfTriplots/fig7_setOfTriplots.pdf\
          $(_6)/_G/fig8_logScoreGrid_modifiedLogScore/fig8_logScoreGrid_modifiedLogScore.pdf\
          $(_6)/_G/fig9_pairedDifferenceInLogScores_modifiedLogScore/fig9_pairedDifferenceInLogScores_modifiedLogScore.pdf\
	  $(_6)/_G/fig10_logScoresForAllEnsembles/fig10_logScoresForAllEnsemble.pdf\
	  ref.bib main.tex latexmkrc
	latexmk main.tex
	$(call timeStamp,$(LOG),"updated manuscript")


$(_6)/_G/fig1_conceptDiagram/fig1_conceptDiagram.pdf:
	cd $(_6)/_G/fig1_conceptDiagram && $(MAKE)

$(_6)/_G/fig2_logScoresFor20102011Training/fig2_logScoresFor20102011Training.pdf :
	cd $(_6)/_G/fig2_logScoresFor20102011Training && $(MAKE)

$(_6)/_G/fig3_triPlot/fig3_triPlotSeason_2017_2018.pdf:
	cd $(_6)/_G/fig3_triPlot && $(MAKE)

$(_6)/_G/fig4_logScoreGrid/fig4_logScoreGrid.pdf:
	cd $(_6)/_G/fig4_logScoreGrid && $(MAKE)

$(_6)/_G/fig5_pairedDifferenceInLogScores/fig5_pairedDifferenceInLogScores.pdf:
	cd $(_6)/_G/fig5_pairedDifferenceInLogScores && $(MAKE)

$(_6)/_G/fig6_logScoresByEpidemicWeek/fig6_logScoresOverEpidemicWeeks.pdf:
	cd $(_6)/_G/fig6_logScoresOverEpidemicWeeks && $(MAKE)

$(_6)/_G/fig7_setOfTriplots/fig7_setOfTriplots.pdf:
	cd $(_6)/_G/fig7_setOfTriplots && $(MAKE)

$(_6)/_G/fig8_logScoreGrid_modifiedLogScore/fig8_logScoreGrid_modifiedLogScore.pdf:
	cd $(_6)/_G/fig8_logScoreGrid_modifiedLogScore && $(MAKE)

$(_6)/_G/fig9_pairedDifferenceInLogScores_modifiedLogScore/fig9_pairedDifferenceInLogScores_modifiedLogScore.pdf:
	cd $(_6)/_G/fig9_pairedDifferenceInLogScores_modifiedLogScore && $(MAKE)

$(_6)/_G/fig10_logScoresForAllEnsembles/fig10_logScoresForAllEnsemble.pdf:
	cd $(_6)/_G/fig10_logScoresForAllEnsemble && $(MAKE)
