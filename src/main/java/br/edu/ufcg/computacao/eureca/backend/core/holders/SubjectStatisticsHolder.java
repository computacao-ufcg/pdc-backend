package br.edu.ufcg.computacao.eureca.backend.core.holders;

import br.edu.ufcg.computacao.eureca.backend.api.http.response.EnrollmentSummary;
import br.edu.ufcg.computacao.eureca.backend.api.http.response.SubjectSummaryResponse;
import br.edu.ufcg.computacao.eureca.backend.core.models.mapentries.*;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class SubjectStatisticsHolder {
    private static SubjectStatisticsHolder instance;
    private Map<IdCode, Collection<IdCode>> enrollmentData;
    private Map<String, Map<IdCode, Collection<IdCode>>> subjectData;
    private Map<String, Collection<SubjectSummaryResponse>> summarizedSubjectData;

    private SubjectStatisticsHolder() {
        retrieveEnrollmentData();
        retrieveSubjectData();
        retrieveSubjectSummary();
    }

    private void retrieveEnrollmentData() {
        this.enrollmentData = new HashMap<>();
        Map<RegistrationEnrollment, StudentPerformance> mapStudentEnrollment = MapsHolder.getInstance().getMap("DiscenteTurma");
        mapStudentEnrollment.forEach((registrationEnrollment, studentPerformance) -> {
            try {
                Collection<IdCode> statusIds;
                IdCode enrollmentId = new IdCode(registrationEnrollment.getEnrollment_id());
                if ((statusIds = this.enrollmentData.get(enrollmentId)) == null) {
                    statusIds = new ArrayList<>();
                }
                statusIds.add(new IdCode(studentPerformance.getStatus_id()));
                this.enrollmentData.put(enrollmentId, statusIds);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    private void retrieveSubjectData() {
        this.subjectData = new HashMap<>();
        Map<IdCode, Enrollment> mapEnrolment = MapsHolder.getInstance().getMap("Turma");
        mapEnrolment.forEach((enrollmentId, enrollment) -> {
            try {
                String term = enrollment.getTerm();
                IdCode subjectIdCode = new IdCode(enrollment.getSubject_id());
                Map<IdCode, Collection<IdCode>> termSubjectData;
                if ((termSubjectData = this.subjectData.get(term)) == null) {
                    termSubjectData = new HashMap<>();
                }
                Collection<IdCode> enrollmentIds;
                if ((enrollmentIds = termSubjectData.get(subjectIdCode)) == null) {
                    enrollmentIds = new ArrayList<>();
                }
                enrollmentIds.add(enrollmentId);
                termSubjectData.put(subjectIdCode, enrollmentIds);
                this.subjectData.put(term, termSubjectData);
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
    }

    private void retrieveSubjectSummary() {
        this.summarizedSubjectData = new HashMap<>();
        this.subjectData.forEach((term, subjectEnrollments) -> {
            try {
                Collection<SubjectSummaryResponse> summary = retrieveSubjectSummaryForTerm(term, subjectEnrollments);
                if (summary != null) {
                    this.summarizedSubjectData.put(term, summary);
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
    }

    private Collection<SubjectSummaryResponse> retrieveSubjectSummaryForTerm(String term, Map<IdCode, Collection<IdCode>> subjectEnrollments) {
        Collection<SubjectSummaryResponse> responses = new ArrayList<>();
        subjectEnrollments.forEach((subjectId, enrollmentIds) -> {
            try {
                Collection<EnrollmentSummary> enrollmentSummary = retrieveSummaryFromEnrollments(enrollmentIds);
                if (enrollmentSummary != null && enrollmentSummary.size() > 0) {
                    SubjectData subjectData = (SubjectData) MapsHolder.getInstance().getValue("Disciplina", subjectId);
                    String subjectName = subjectData.getName();
                    String subjectCode = subjectData.getCode();
                    SubjectSummaryResponse subjectSummary = new SubjectSummaryResponse(term, subjectCode, subjectName, enrollmentSummary);
                    responses.add(subjectSummary);
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
        return responses;
    }

    private Collection<EnrollmentSummary> retrieveSummaryFromEnrollments(Collection<IdCode> enrollments) {
        Collection<EnrollmentSummary> enrollmentSummaries = new ArrayList<>();
        enrollments.forEach(enrollment -> {
            try {
                int passed = 0;
                int failed = 0;
                int absent = 0;
                int dropout = 0;
                Collection<IdCode> status = this.enrollmentData.get(enrollment);
                if (status != null) {
                    for (IdCode studentStatus : status) {
                        switch (studentStatus.getId()) {
                            case 1:
                                passed++;
                                break;
                            case 5:
                                failed++;
                                break;
                            case 6:
                                absent++;
                                break;
                            case 7:
                                dropout++;
                                break;
                        }
                    }
                    EnrollmentSummary enrollmentSummary = new EnrollmentSummary(passed, failed, absent, dropout);
                    enrollmentSummaries.add(enrollmentSummary);
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
        return enrollmentSummaries;
    }

    public static synchronized SubjectStatisticsHolder getInstance() {
        if (instance == null) {
            instance = new SubjectStatisticsHolder();
        }
        return instance;
    }

    public Map<String, Collection<SubjectSummaryResponse>> getSubjectSummary() {
        return this.summarizedSubjectData;
    }

    public void printEnrollmentData() {
        this.enrollmentData.forEach((enrollmentId, statusList) -> {
            System.out.print("enrollmentId: " + enrollmentId.getId() + " [");
            statusList.forEach(status -> {
                System.out.print(status.getId() + ":");
            });
            System.out.println("]");
        });
    }

    public void printSubjectData() {
        this.subjectData.forEach((term, enrollments) -> {
            System.out.println("Term: " + term);
            enrollments.forEach((code, enrollmentIds) -> {
                System.out.print("Code: " + code + " -> [");
                enrollmentIds.forEach(enrollment -> {
                    System.out.print(enrollment.getId() + ":");
                });
                System.out.println("]");
            });
        });
    }
}
