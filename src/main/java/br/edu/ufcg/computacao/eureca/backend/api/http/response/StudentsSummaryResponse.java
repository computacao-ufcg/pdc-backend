package br.edu.ufcg.computacao.eureca.backend.api.http.response;

import br.edu.ufcg.computacao.eureca.backend.constants.GlossaryFields;

public class StudentsSummaryResponse {
    private ActivesSummary activesSummary;
    private AlumniSummary alumniSummary;
    private DelayedSummary delayedSummary;
    private DropoutsSummary dropoutsSummary;
    private GlossaryFields glossary;

    public StudentsSummaryResponse(ActivesSummary activesSummary, AlumniSummary alumniSummary,
                                   DelayedSummary delayedSummary, DropoutsSummary dropoutsSummary) {
        this.activesSummary = activesSummary;
        this.alumniSummary = alumniSummary;
        this.delayedSummary = delayedSummary;
        this.dropoutsSummary = dropoutsSummary;
    }

    public ActivesSummary getActivesSummary() {
        return activesSummary;
    }

    public void setActivesSummary(ActivesSummary activesSummary) {
        this.activesSummary = activesSummary;
    }

    public AlumniSummary getAlumniSummary() {
        return alumniSummary;
    }

    public void setAlumniSummary(AlumniSummary alumniSummary) {
        this.alumniSummary = alumniSummary;
    }

    public DelayedSummary getDelayedSummary() {
        return delayedSummary;
    }

    public void setDelayedSummary(DelayedSummary delayedSummary) {
        this.delayedSummary = delayedSummary;
    }

    public DropoutsSummary getDropoutsSummary() {
        return dropoutsSummary;
    }

    public void setDropoutsSummary(DropoutsSummary dropoutsSummary) {
        this.dropoutsSummary = dropoutsSummary;
    }

    public GlossaryFields getGlossary() {
        return glossary;
    }

    public void setGlossary(GlossaryFields glossary) {
        this.glossary = glossary;
    }
}
