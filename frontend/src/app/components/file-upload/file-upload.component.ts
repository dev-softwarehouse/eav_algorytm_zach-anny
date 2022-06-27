import { Component, OnInit } from '@angular/core';
import { FileUploadService } from 'src/app/services/file-upload.service';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css'],
})
export class FileUploadComponent implements OnInit {
  loading: boolean = false; // Flag variable
  file: File | undefined; // Variable to store file
  numberOfRows: any;
  fileName: string | undefined;
  numberOfAttributes: number | undefined;
  minimumRuleLength: number | undefined;
  maximumRuleLength: number | undefined;
  rulesLength: number | undefined;
  ruleUniqueness: number | undefined;

  // Inject service
  constructor(private fileUploadService: FileUploadService) {}

  ngOnInit(): void {}

  // On file Select
  onChange(event: any) {
    this.file = event.target.files[0];
    this.fileName = event.target.files[0].name;
  }

  // OnClick of button Upload
  onUpload() {
    this.loading = !this.loading;
    console.log(this.file);
    this.fileUploadService.upload(this.file).subscribe((response: any) => {
      console.log({ api_response: response });
      this.loading = false;
      this.numberOfRows = response.number_of_rows;
      this.fileName = response.file_name;
      this.numberOfAttributes = response.attributes.length-1;
      this.minimumRuleLength = response.rule_length.min_rule_length;
      this.maximumRuleLength = response.rule_length.max_rule_length;
      this.rulesLength = response.rules.length;
      this.ruleUniqueness = response.rule_uniqueness.length;
    });
  }
}
